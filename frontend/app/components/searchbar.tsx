'use client';

import { useState } from 'react';
import { Search, Loader2 } from 'lucide-react';

interface SearchBarProps {
  onSearch: (query: string) => void;
  isLoading?: boolean;
  placeholder?: string;
}

export default function SearchBar({ onSearch, isLoading = false, placeholder = "Search for products..." }: SearchBarProps) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl mx-auto">
      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          {isLoading ? (
            <Loader2 className="h-5 w-5 text-gray-400 animate-spin" />
          ) : (
            <Search className="h-5 w-5 text-gray-400" />
          )}
        </div>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={placeholder}
          disabled={isLoading}
          className="block w-full pl-10 pr-12 py-3 border border-gray-300 rounded-lg leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-transparent text-lg disabled:opacity-50"
        />
        <div className="absolute inset-y-0 right-0 flex items-center">
          <button
            type="submit"
            disabled={isLoading || !query.trim()}
            className="inline-flex items-center px-4 py-2 mr-1 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? 'Searching...' : 'Search'}
          </button>
        </div>
      </div>
      
      {/* Quick search suggestions */}
      <div className="mt-3 flex flex-wrap gap-2 justify-center">
        <span className="text-sm text-gray-500">Try:</span>
        {[
          'comfortable running shoes',
          'budget laptop for students', 
          'wireless headphones with bass'
        ].map((suggestion) => (
          <button
            key={suggestion}
            type="button"
            onClick={() => {
              setQuery(suggestion);
              onSearch(suggestion);
            }}
            className="text-sm text-blue-600 hover:text-blue-800 underline"
          >
            "{suggestion}"
          </button>
        ))}
      </div>
    </form>
  );
}