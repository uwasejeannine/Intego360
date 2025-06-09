import React, { useState, useRef, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  HomeIcon,
  ChartBarIcon,
  HeartIcon,
  AcademicCapIcon,
  ExclamationTriangleIcon,
  UsersIcon,
  MapPinIcon,
  BuildingLibraryIcon,
  BuildingOffice2Icon,
  UserGroupIcon,
  Bars3Icon,
} from '@heroicons/react/24/outline';

const sectors = [
  { name: 'Agriculture', value: 'agriculture', icon: ChartBarIcon, href: '/agriculture' },
  { name: 'Health', value: 'health', icon: HeartIcon, href: '/health' },
  { name: 'Education', value: 'education', icon: AcademicCapIcon, href: '/education' },
];

const quickLinks = [
  { name: 'Dashboard', href: '/dashboard', icon: HomeIcon },
  { name: 'Alerts', href: '/alerts', icon: ExclamationTriangleIcon },
];

type Sector = 'agriculture' | 'health' | 'education';

type SectorNavLink = { name: string; href: string; icon: React.ComponentType<any> };

const sectorNav: Record<Sector, SectorNavLink[]> = {
  agriculture: [
    { name: 'Overview', href: '/agriculture', icon: ChartBarIcon },
    { name: 'Farmers', href: '/farmers', icon: UsersIcon }, // Updated to match your routing
    { name: 'Crops', href: '/agriculture/crops', icon: MapPinIcon },
    { name: 'Cooperatives', href: '/agriculture/cooperatives', icon: UserGroupIcon },
  ],
  health: [
    { name: 'Overview', href: '/health', icon: HeartIcon },
    { name: 'Facilities', href: '/health/facilities', icon: BuildingOffice2Icon },
    { name: 'Diseases', href: '/health/diseases', icon: ExclamationTriangleIcon },
    { name: 'Vaccination', href: '/health/vaccination', icon: UserGroupIcon },
  ],
  education: [
    { name: 'Overview', href: '/education', icon: AcademicCapIcon },
    { name: 'Schools', href: '/education/schools', icon: BuildingLibraryIcon },
    { name: 'Students', href: '/education/students', icon: UsersIcon },
    { name: 'Teachers', href: '/education/teachers', icon: UserGroupIcon },
  ],
};

const Sidebar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [selectedSector, setSelectedSector] = useState<Sector | null>(null);
  const [sectorDropdownOpen, setSectorDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Determine current sector from URL - Updated to include farmers page
  let currentSector: Sector | null = null;
  if (location.pathname.startsWith('/agriculture') || location.pathname === '/farmers') {
    currentSector = 'agriculture';
  } else if (location.pathname.startsWith('/health')) {
    currentSector = 'health';
  } else if (location.pathname.startsWith('/education')) {
    currentSector = 'education';
  }

  // Set selected sector based on current route
  useEffect(() => {
    if (currentSector && selectedSector !== currentSector) {
      setSelectedSector(currentSector);
    }
  }, [currentSector, selectedSector]);

  // Close dropdown on outside click
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setSectorDropdownOpen(false);
      }
    }
    if (sectorDropdownOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    } else {
      document.removeEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [sectorDropdownOpen]);

  const handleSectorSelect = (sector: Sector) => {
    setSelectedSector(sector);
    setSectorDropdownOpen(false);
    navigate(sectors.find(s => s.value === sector)?.href || '/dashboard');
  };

  return (
    <aside className="bg-white min-h-screen w-64 flex flex-col shadow-lg border-r border-gray-200">
      {/* Navigation */}
      <nav className="flex-1 px-4 py-6 space-y-6">
        {/* Quick Links */}
        <div>
          <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">
            Quick Access
          </h3>
          <div className="space-y-1">
            {quickLinks.map(link => (
              <button
                key={link.name}
                onClick={() => navigate(link.href)}
                className={`group flex items-center w-full px-3 py-2 text-sm font-medium rounded-lg transition-colors duration-150 ${
                  location.pathname === link.href
                    ? 'bg-[#137775] text-white'
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                <link.icon className="flex-shrink-0 h-5 w-5 mr-3" />
                {link.name}
              </button>
            ))}
          </div>
        </div>

        {/* Sectors Dropdown */}
        <div>
          <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">
            Sectors
          </h3>
          <div className="relative" ref={dropdownRef}>
            <button
              onClick={() => setSectorDropdownOpen(!sectorDropdownOpen)}
              className="group flex items-center justify-between w-full px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-lg transition-colors duration-150"
            >
              <div className="flex items-center">
                <Bars3Icon className="flex-shrink-0 h-5 w-5 mr-3" />
                <span>
                  {selectedSector 
                    ? sectors.find(s => s.value === selectedSector)?.name 
                    : 'Select Sector'
                  }
                </span>
              </div>
              <svg 
                className={`h-4 w-4 transition-transform ${sectorDropdownOpen ? 'rotate-180' : ''}`} 
                fill="none" 
                viewBox="0 0 24 24" 
                stroke="currentColor"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            {/* Dropdown Menu */}
            {sectorDropdownOpen && (
              <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-gray-200 rounded-lg shadow-lg z-50">
                {sectors.map(sector => (
                  <button
                    key={sector.value}
                    onClick={() => handleSectorSelect(sector.value as Sector)}
                    className={`flex items-center w-full px-3 py-2 text-sm hover:bg-gray-100 first:rounded-t-lg last:rounded-b-lg ${
                      selectedSector === sector.value
                        ? 'bg-[#137775] text-white hover:bg-[#137775]'
                        : 'text-gray-700'
                    }`}
                  >
                    <sector.icon className="flex-shrink-0 h-5 w-5 mr-3" />
                    {sector.name}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Sector Navigation - Show when dropdown is open OR when currently on a sector page */}
        {selectedSector && (sectorDropdownOpen || currentSector) && (
          <div>
            <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">
              {selectedSector.charAt(0).toUpperCase() + selectedSector.slice(1)} Navigation
            </h3>
            <div className="space-y-1">
              {sectorNav[selectedSector].map((link: SectorNavLink) => (
                <button
                  key={link.name}
                  onClick={() => navigate(link.href)}
                  className={`group flex items-center w-full px-3 py-2 text-sm font-medium rounded-lg transition-colors duration-150 ${
                    location.pathname === link.href
                      ? 'bg-[#137775] text-white'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  <link.icon className="flex-shrink-0 h-5 w-5 mr-3" />
                  {link.name}
                </button>
              ))}
            </div>
          </div>
        )}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-gray-200">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
            <span className="text-gray-600 text-xs font-medium">RM</span>
          </div>
          <div className="flex-1">
            <p className="text-sm font-medium text-gray-900">Ruth Mutabazi</p>
            <p className="text-xs text-gray-500">Administrator</p>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;