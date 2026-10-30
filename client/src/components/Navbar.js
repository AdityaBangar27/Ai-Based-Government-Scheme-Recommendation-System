import React from 'react';
import { Link } from 'react-router-dom';
import { Award } from 'react-feather';

const Navbar = () => {
  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-40 shadow-xs">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2.5">
            <div className="w-9 h-9 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-xl flex items-center justify-center text-white shadow-sm">
              <Award size={20} />
            </div>
            <div>
              <span className="font-extrabold text-lg text-gray-900 tracking-tight">
                GovScheme<span className="text-cyan-600">.AI</span>
              </span>
              <span className="hidden sm:inline-block ml-2 text-[11px] font-semibold bg-cyan-50 text-cyan-700 px-2 py-0.5 rounded-full border border-cyan-200">
                Scheme Recommendation
              </span>
            </div>
          </Link>

          {/* Right badge */}
          <div className="flex items-center space-x-3 text-xs">
            <span className="inline-flex items-center gap-1 px-3 py-1 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-full font-medium">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              <span>ML Engine Active</span>
            </span>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
