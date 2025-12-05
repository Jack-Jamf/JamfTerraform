use std::process::Stdio;
use tokio::io::{AsyncBufReadExt, BufReader};
use tokio::process::Command;
use std::io::Write;
use tauri::Emitter;

#[derive(serde::Serialize, Clone)]
struct TerraformOutput {
    line: String,
    stream: String, // "stdout" or "stderr"
}

#[tauri::command]
async fn run_terraform(
    app: tauri::AppHandle,
    hcl_code: String,
    jamf_url: String,
    jamf_username: String,
    jamf_password: String,
) -> Result<String, String> {
    // Create temporary directory for Terraform files
    let temp_dir = tempfile::tempdir()
        .map_err(|e| format!("Failed to create temp directory: {}", e))?;
    
    let tf_file_path = temp_dir.path().join("main.tf");
    
    // Write HCL code to temporary main.tf file
    let mut file = std::fs::File::create(&tf_file_path)
        .map_err(|e| format!("Failed to create main.tf: {}", e))?;
    
    file.write_all(hcl_code.as_bytes())
        .map_err(|e| format!("Failed to write HCL code: {}", e))?;
    
    // Step 1: Run terraform init to download providers
    let init_output = Command::new("terraform")
        .arg("init")
        .current_dir(temp_dir.path())
        .output()
        .await
        .map_err(|e| format!("Failed to run terraform init: {}", e))?;
    
    if !init_output.status.success() {
        let stderr = String::from_utf8_lossy(&init_output.stderr);
        return Err(format!("Terraform init failed: {}", stderr));
    }
    
    // Step 2: Execute terraform apply with Jamf credentials as environment variables
    let mut child = Command::new("terraform")
        .arg("apply")
        .arg("-auto-approve")
        .current_dir(temp_dir.path())
        .env("JAMF_URL", jamf_url)           // Never logged
        .env("JAMF_USERNAME", jamf_username) // Never logged
        .env("JAMF_PASSWORD", jamf_password) // Never logged
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .map_err(|e| format!("Failed to spawn terraform: {}", e))?;
    
    // Get stdout and stderr handles
    let stdout = child.stdout.take()
        .ok_or("Failed to capture stdout")?;
    let stderr = child.stderr.take()
        .ok_or("Failed to capture stderr")?;
    
    // Clone app handle for async tasks
    let app_stdout = app.clone();
    let app_stderr = app.clone();
    
    // Stream stdout in real-time
    let stdout_task = tokio::spawn(async move {
        let reader = BufReader::new(stdout);
        let mut lines = reader.lines();
        
        while let Ok(Some(line)) = lines.next_line().await {
            let output = TerraformOutput {
                line: line.clone(),
                stream: "stdout".to_string(),
            };
            // Emit event to frontend
            let _ = app_stdout.emit("terraform-output", output);
        }
    });
    
    // Stream stderr in real-time
    let stderr_task = tokio::spawn(async move {
        let reader = BufReader::new(stderr);
        let mut lines = reader.lines();
        
        while let Ok(Some(line)) = lines.next_line().await {
            let output = TerraformOutput {
                line: line.clone(),
                stream: "stderr".to_string(),
            };
            // Emit event to frontend
            let _ = app_stderr.emit("terraform-output", output);
        }
    });
    
    // Wait for both streaming tasks to complete
    let _ = tokio::try_join!(stdout_task, stderr_task);
    
    // Wait for terraform process to complete
    let status = child.wait().await
        .map_err(|e| format!("Failed to wait for terraform: {}", e))?;
    
    // Clean up temp directory
    drop(temp_dir);
    
    if status.success() {
        Ok("Terraform apply completed successfully".to_string())
    } else {
        Err(format!("Terraform apply failed with exit code: {:?}", status.code()))
    }
}

#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![greet, run_terraform])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
