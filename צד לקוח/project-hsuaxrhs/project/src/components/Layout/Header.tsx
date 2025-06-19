import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Beaker, LogOut } from 'lucide-react';
import { useAuth } from '../../context/auth';

const Header: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center">
              <Beaker className="h-8 w-8 text-blue-600" />
              <span className="ml-2 text-xl font-bold text-gray-900">AromaID</span>
            </Link>
          </div>
          
          {user && (
            <div className="flex items-center">
              <nav className="hidden md:flex space-x-8 mr-8">
                <Link
                  to="/dashboard"
                  className="text-gray-700 hover:text-blue-600 px-3 py-2 text-sm font-medium"
                >
                  Dashboard
                </Link>
                <Link
                  to="/upload"
                  className="text-gray-700 hover:text-blue-600 px-3 py-2 text-sm font-medium"
                >
                  Upload Data
                </Link>
                <Link
                  to="/predict"
                  className="text-gray-700 hover:text-blue-600 px-3 py-2 text-sm font-medium"
                >
                  Predict
                </Link>
              </nav>
              <div className="flex items-center">
                <span className="text-sm text-gray-700 mr-4 hidden md:block">
                  {user.username}
                </span>
                <button
                  onClick={handleLogout}
                  className="flex items-center text-gray-700 hover:text-red-600"
                >
                  <LogOut className="h-5 w-5" />
                  <span className="ml-1 text-sm hidden md:block">Logout</span>
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;