import { useEffect, useState } from 'react';
import { FaMoon, FaSun } from 'react-icons/fa';

const DarkModeToggle = () => {
  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem('theme') === 'dark';
  });

  useEffect(() => {
    const root = window.document.documentElement;
    if (darkMode) {
      root.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      root.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [darkMode]);

  return (
    <button
      onClick={() => setDarkMode(!darkMode)}
      className="text-xl p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-900 transition"
      title="Toggle dark mode"
    >
      {darkMode ? <FaSun className="text-yellow-400" /> : <FaMoon className="text-gray-900" />}
    </button>
  );
};

export default DarkModeToggle;
