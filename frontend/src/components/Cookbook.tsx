import React, { useState, useEffect } from 'react';
import { ExecutionService } from '../services/ExecutionService';
import type { CookbookModule } from '../types';
import './Cookbook.css';

interface CookbookProps {
  onRecipeSelect?: (prompt: string) => void;
}

const Cookbook: React.FC<CookbookProps> = ({ onRecipeSelect }) => {
  const [modules, setModules] = useState<CookbookModule[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCookbook = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await ExecutionService.getCookbook();
        setModules(data.modules);
      } catch (err) {
        setError('Failed to load cookbook');
        console.error('Error fetching cookbook:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchCookbook();
  }, []);

  const handleRecipeClick = (recipe: CookbookModule) => {
    if (onRecipeSelect) {
      onRecipeSelect(recipe.prompt);
    }
  };

  return (
    <div className="cookbook-container">
      <div className="cookbook-header">
        <h1 className="cookbook-title">Recipe Cookbook</h1>
        <p className="cookbook-description">
          Pre-built templates for common Jamf configurations. Click any recipe to generate the Terraform HCL.
        </p>
      </div>

      {loading ? (
        <div className="empty-cookbook">
          <div className="empty-cookbook-icon">⏳</div>
          <h2 className="empty-cookbook-title">Loading Cookbook...</h2>
        </div>
      ) : error ? (
        <div className="empty-cookbook">
          <div className="empty-cookbook-icon">⚠️</div>
          <h2 className="empty-cookbook-title">Failed to Load Cookbook</h2>
          <p>{error}</p>
        </div>
      ) : modules.length === 0 ? (
        <div className="empty-cookbook">
          <div className="empty-cookbook-icon">📚</div>
          <h2 className="empty-cookbook-title">No Recipes Available</h2>
        </div>
      ) : (
        <div className="cookbook-grid">
          {modules.map((recipe) => (
            <div
              key={recipe.id}
              className="cookbook-card"
              onClick={() => handleRecipeClick(recipe)}
            >
              <div className="cookbook-card-header">
                <div className="cookbook-card-icon">{recipe.icon}</div>
                <div>
                  <div className="cookbook-card-category">{recipe.category}</div>
                  <h3 className="cookbook-card-title">{recipe.title}</h3>
                </div>
              </div>

              <p className="cookbook-card-description">{recipe.description}</p>

              <div className="cookbook-card-footer">
                <div className="cookbook-card-tags">
                  {recipe.tags.map((tag) => (
                    <span key={tag} className="cookbook-tag">
                      {tag}
                    </span>
                  ))}
                </div>
                <div className="cookbook-card-action">
                  <span>Use Recipe</span>
                  <span>→</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Cookbook;
