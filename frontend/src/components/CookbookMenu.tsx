import React, { useState, useEffect } from 'react';
import { ExecutionService } from '../services/ExecutionService';
import type { CookbookModule } from '../types';
import './CookbookMenu.css';

interface CookbookMenuProps {
  onRecipeSelect?: (prompt: string) => void;
}

const CookbookMenu: React.FC<CookbookMenuProps> = ({ onRecipeSelect }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [modules, setModules] = useState<CookbookModule[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isExpanded && modules.length === 0) {
      fetchCookbook();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isExpanded]);

  const fetchCookbook = async () => {
    setLoading(true);
    try {
      const data = await ExecutionService.getCookbook();
      setModules(data.modules);
    } catch (err) {
      console.error('Error fetching cookbook:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRecipeClick = (recipe: CookbookModule) => {
    if (onRecipeSelect) {
      onRecipeSelect(recipe.prompt);
      setIsExpanded(false);
    }
  };

  return (
    <div className="cookbook-menu-wrapper">
      <button
        className="cookbook-menu-button"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        📚 Recipes
      </button>

      {isExpanded && (
        <div className="cookbook-menu-dropdown">
          <div className="dropdown-header">
            <h3>📚 Recipe Cookbook</h3>
            <button
              className="close-btn"
              onClick={(e) => {
                e.stopPropagation();
                setIsExpanded(false);
              }}
            >
              ✕
            </button>
          </div>

          <div className="cookbook-menu-content">
            {loading ? (
              <div className="cookbook-loading">⏳ Loading recipes...</div>
            ) : modules.length === 0 ? (
              <div className="cookbook-empty">No recipes available</div>
            ) : (
              <div className="recipe-list">
                {modules.map((recipe) => (
                  <div
                    key={recipe.id}
                    className="recipe-item"
                    onClick={() => handleRecipeClick(recipe)}
                  >
                    <div className="recipe-header">
                      <span className="recipe-icon">{recipe.icon}</span>
                      <div className="recipe-info">
                        <div className="recipe-title">{recipe.title}</div>
                        <div className="recipe-category">{recipe.category}</div>
                      </div>
                    </div>
                    <div className="recipe-description">{recipe.description}</div>
                    <div className="recipe-tags">
                      {recipe.tags.map((tag) => (
                        <span key={tag} className="recipe-tag">
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default CookbookMenu;
