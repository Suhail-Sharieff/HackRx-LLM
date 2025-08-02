import React from 'react';
import { useNavigate } from 'react-router-dom';
import { SplineLight, SplineDark } from './Spline.jsx';
import { FaUpload, FaSearch, FaMagic, FaQuestion } from 'react-icons/fa';

const HomePage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-white dark:bg-black px-6 py-12 md:px-16 lg:px-24 flex flex-col lg:flex-row items-center justify-between text-gray-900 dark:text-white">
      {/* Left Content */}
      <div className="flex flex-col space-y-6 max-w-xl">
        <h1 className="text-4xl md:text-5xl font-bold">
          Welcome to <span className="text-blue-600">Parse AI</span>
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-300">
          Your intelligent assistant to analyze, extract, and understand documents with the power of AI.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Feature icon={<FaUpload />} title="Upload PDFs & Images" />
          <Feature icon={<FaMagic />} title="Auto Summarization" />
          <Feature icon={<FaSearch />} title="Smart Querying" />
          <Feature icon={<FaQuestion />} title="Ask Anything About the File" />
        </div>

        <button
          onClick={() => navigate('/app')}
          className="px-6 py-3 bg-blue-600 dark:bg-blue-500 text-white font-semibold rounded-lg hover:bg-blue-700 dark:hover:bg-blue-600 transition"
        >
          Get Started
        </button>
      </div>

      {/* Right Visual */}
      <div className="mt-10 lg:mt-0">
        <div className="block dark:hidden">
          <SplineLight />
        </div>
        <div className="hidden dark:block">
          <SplineDark />
        </div>
      </div>
    </div>
  );
};

const Feature = ({ icon, title }) => (
  <div className="flex items-center space-x-3 bg-gray-100 dark:bg-[#111111] px-4 py-3 rounded-lg shadow-sm">
    <div className="text-blue-600 text-xl">{icon}</div>
    <div className="text-gray-800 dark:text-white font-medium">{title}</div>
  </div>
);

export default HomePage;
