import React, { useState, useRef, useEffect } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import Sidebar from './Sidebar';
import {
  Bars3Icon,
  BellIcon,
  QuestionMarkCircleIcon,
  ChevronDownIcon,
  ChartBarIcon,
  HeartIcon,
  AcademicCapIcon,
} from '@heroicons/react/24/outline';
import { useSector, Sector } from '../../contexts/SectorContext';



const quickLinks = [
  { name: 'Dashboard', href: '/dashboard' },
  { name: 'Alerts', href: '/alerts' },
  { name: 'Reports', href: '/reports' },
  { name: 'Settings', href: '/settings' },
];

const DashboardLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, logout } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { sector, setSector } = useSector();

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Top header - Full width */}
      <Header 
        user={user} 
        onLogout={logout} 
        onMobileMenuToggle={() => setMobileMenuOpen(true)}
        sector={sector}
        setSector={setSector}
      />
      
      {/* Content area with sidebar and main content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <div className="hidden md:flex md:flex-shrink-0">
          <Sidebar />
        </div>
        
        {/* Main content area */}
        <div className="flex flex-col flex-1 overflow-hidden">
          {/* Main content */}
          <main className="flex-1 relative overflow-y-auto focus:outline-none">
            <div className="py-6">
              <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
                {children}
              </div>
            </div>
          </main>
        </div>
      </div>
    </div>
  );
};

const Header: React.FC<{
  user: any;
  onLogout: () => void;
  onMobileMenuToggle: () => void;
  sector: Sector;
  setSector: (sector: Sector) => void;
}> = ({ user, onLogout, onMobileMenuToggle, sector, setSector }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const [userDropdownOpen, setUserDropdownOpen] = useState(false);
  const [sectorDropdownOpen, setSectorDropdownOpen] = useState(false);
  const userDropdownRef = useRef<HTMLDivElement>(null);
  const sectorDropdownRef = useRef<HTMLDivElement>(null);

  const getPageTitle = () => {
    const path = location.pathname;
    switch (path) {
      case '/dashboard':
        return 'Dashboard';
      case '/agriculture':
        return 'Agriculture';
      case '/health':
        return 'Health';
      case '/education':
        return 'Education';
      case '/alerts':
        return 'Alerts';
      case '/reports':
        return 'Reports';
      case '/settings':
        return 'Settings';
      default:
        return 'Dashboard';
    }
  };

  // Close dropdowns on outside click
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (userDropdownRef.current && !userDropdownRef.current.contains(event.target as Node)) {
        setUserDropdownOpen(false);
      }
      if (sectorDropdownRef.current && !sectorDropdownRef.current.contains(event.target as Node)) {
        setSectorDropdownOpen(false);
      }
    }
    if (userDropdownOpen || sectorDropdownOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    } else {
      document.removeEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [userDropdownOpen, sectorDropdownOpen]);

  // User initials for avatar
  const initials = user?.full_name
    ? user.full_name.split(' ').map((n: string) => n[0]).join('').toUpperCase().slice(0, 2)
    : 'RM';

 

  return (
    <div className="relative z-10 flex-shrink-0 flex h-16 bg-[#137775] shadow items-center px-4 w-full">
      {/* Left side - Brand Logo and sector selection */}
      <div className="flex items-center space-x-4">
        {/* Brand Logo */}
        <div className="flex items-center space-x-3">
          <div className="flex items-center justify-center w-8 h-8 bg-white bg-opacity-20 rounded">
            <span className="text-white font-bold text-sm">I</span>
          </div>
          <span className="text-white text-xl font-bold hidden sm:block">Intego360</span>
        </div>
      </div>

      {/* Center - Page title */}
      <div className="flex-1 flex justify-center">
        <h1 className="text-lg font-semibold text-white">{getPageTitle()}</h1>
      </div>

      {/* Right side - Actions and user menu */}
      <div className="flex items-center space-x-3">
        {/* Notifications */}
        <button className="text-white p-2 hover:bg-[#0f6562] rounded-md relative transition-colors duration-150">
          <BellIcon className="h-5 w-5" />
          <span className="absolute -top-1 -right-1 h-4 w-4 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
            3
          </span>
        </button>

        {/* Help */}
        <button className="text-white p-2 hover:bg-[#0f6562] rounded-md transition-colors duration-150">
          <QuestionMarkCircleIcon className="h-5 w-5" />
        </button>

        {/* User Profile Dropdown */}
        <div className="relative" ref={userDropdownRef}>
          <button
            className="flex items-center space-x-2 text-white hover:bg-[#0f6562] px-3 py-2 rounded-md focus:outline-none transition-colors duration-150"
            onClick={() => setUserDropdownOpen(!userDropdownOpen)}
          >
            <div className="flex items-center justify-center h-8 w-8 rounded-full bg-white bg-opacity-20 text-white font-bold text-sm">
              {initials}
            </div>
            <span className="font-medium text-sm hidden sm:block">{user?.full_name || 'User'}</span>
            <ChevronDownIcon className={`h-4 w-4 transition-transform duration-150 ${userDropdownOpen ? 'rotate-180' : ''}`} />
          </button>

          {/* User Dropdown Menu */}
          {userDropdownOpen && (
            <div className="absolute right-0 top-12 w-72 bg-white rounded-lg shadow-xl py-2 z-50 border border-gray-200">
              {/* User Info Header */}
              <div className="flex items-center px-4 py-3 border-b border-gray-100">
                <div className="flex items-center justify-center h-10 w-10 rounded-full bg-[#137775] bg-opacity-10 text-[#137775] font-bold text-sm mr-3">
                  {initials}
                </div>
                <div>
                  <p className="font-medium text-gray-900 text-sm">{user?.full_name || 'User'}</p>
                  <p className="text-xs text-gray-500">{user?.role || 'Administrator'}</p>
                </div>
              </div>

              {/* Language Selector */}
              <div className="px-4 py-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-700">Language</span>
                  <div className="flex items-center space-x-1 text-sm text-gray-600">
                    <img src="/api/placeholder/16/12" alt="US Flag" className="w-4 h-3" />
                    <span>En</span>
                    <ChevronDownIcon className="h-3 w-3" />
                  </div>
                </div>
              </div>

              <div className="border-t border-gray-100 py-1">
                <button
                  className="flex items-center w-full px-4 py-2 text-gray-700 hover:bg-gray-50 text-sm transition-colors duration-150"
                  onClick={() => { setUserDropdownOpen(false); navigate('/profile'); }}
                >
                  Profile Settings
                </button>
                <button
                  className="flex items-center w-full px-4 py-2 text-gray-700 hover:bg-gray-50 text-sm transition-colors duration-150"
                  onClick={() => { setUserDropdownOpen(false); navigate('/settings'); }}
                >
                  Account Settings
                </button>
                <button
                  className="flex items-center w-full px-4 py-2 text-red-600 hover:bg-red-50 text-sm transition-colors duration-150"
                  onClick={() => { setUserDropdownOpen(false); onLogout(); }}
                >
                  Sign Out
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DashboardLayout;