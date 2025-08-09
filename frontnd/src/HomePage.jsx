import React, { useState } from 'react';
import { Upload, MessageSquare, FlaskConical, Database, Search, Settings, Home, FileText, Users, Zap } from 'lucide-react';
import { FaUpload, FaSearch, FaMagic, FaQuestion } from 'react-icons/fa';
import { SplineLight, SplineDark } from './Spline.jsx';

const API = import.meta.env.VITE_API_BASE_URL;

// Loading spinner component
const LoadingSpinner = () => (
  <div className="flex justify-center items-center py-4">
    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
  </div>
);

// Section component for styled cards
const Section = ({ title, content }) => (
  <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 p-6 rounded-2xl shadow-lg">
    <h3 className="text-xl font-semibold mb-3 text-blue-600 dark:text-blue-400">{title}</h3>
    <div className="space-y-2 text-gray-700 dark:text-gray-300">
      {Array.isArray(content) ? content.map((item, index) => (
        <p key={index}>{item}</p>
      )) : (
        <p>{content}</p>
      )}
    </div>
  </div>
);

// Tab component
const Tab = ({ active, onClick, children, icon: Icon }) => (
  <button
    onClick={onClick}
    className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all duration-200 ${
      active 
        ? 'bg-blue-600 text-white shadow-md' 
        : 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
    }`}
  >
    <Icon size={20} />
    <span>{children}</span>
  </button>
);

// Feature component for home page
const Feature = ({ icon, title }) => (
  <div className="flex items-center space-x-3 bg-gray-100 dark:bg-[#111111] px-4 py-3 rounded-lg shadow-sm">
    <div className="text-blue-600 text-xl">{icon}</div>
    <div className="text-gray-800 dark:text-white font-medium">{title}</div>
  </div>
);

export default function HomePage() {
  const [activeTab, setActiveTab] = useState('home');
  
  // File upload state
  const [file, setFile] = useState(null);
  const [uploadResult, setUploadResult] = useState(null);
  const [isLoadingUpload, setIsLoadingUpload] = useState(false);
  
  // Q&A state
  const [context, setContext] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [isLoadingAsk, setIsLoadingAsk] = useState(false);
  
  // Simulation state
  const [scenario, setScenario] = useState("");
  const [simulation, setSimulation] = useState("");
  const [isLoadingSimulate, setIsLoadingSimulate] = useState(false);
  
  // Vector database state
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [isLoadingSearch, setIsLoadingSearch] = useState(false);
  const [vectorStats, setVectorStats] = useState(null);
  

  
  // Error state
  const [error, setError] = useState(null);

  // API handlers
  const handleFileUpload = async () => {
    if (!file) {
      setError("Please choose a file to upload.");
      return;
    }

    setIsLoadingUpload(true);
    setError(null);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${API}/upload`, { method: "POST", body: formData });
      if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);
      const data = await res.json();
      setUploadResult(data);
      setContext(data.full_text);
    } catch (err) {
      console.error("Upload failed:", err);
      setError(`Failed to upload file. Please check the API server.`);
    } finally {
      setIsLoadingUpload(false);
    }
  };

  const handleAsk = async () => {
    if (!question) {
      setError("Please enter a question.");
      return;
    }
    
    setIsLoadingAsk(true);
    setError(null);
    try {
      const res = await fetch(`${API}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ context, question }),
      });
      if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);
      const data = await res.json();
      setAnswer(data.answer);
    } catch (err) {
      console.error("Ask request failed:", err);
      setError(`Failed to get an answer. Please check the API server.`);
    } finally {
      setIsLoadingAsk(false);
    }
  };

  const handleSimulate = async () => {
    if (!scenario) {
      setError("Please enter a scenario.");
      return;
    }
    
    setIsLoadingSimulate(true);
    setError(null);
    try {
      const res = await fetch(`${API}/simulate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ context, scenario }),
      });
      if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);
      const data = await res.json();
      setSimulation(data.result);
    } catch (err) {
      console.error("Simulation request failed:", err);
      setError(`Failed to run the simulation. Please check the API server.`);
    } finally {
      setIsLoadingSimulate(false);
    }
  };

  const handleVectorSearch = async () => {
    if (!searchQuery) {
      setError("Please enter a search query.");
      return;
    }
    
    setIsLoadingSearch(true);
    setError(null);
    try {
      const res = await fetch(`${API}/vector/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: searchQuery, n_results: 5 }),
      });
      if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);
      const data = await res.json();
      setSearchResults(data.results);
    } catch (err) {
      console.error("Vector search failed:", err);
      setError(`Failed to search documents. Please check the API server.`);
    } finally {
      setIsLoadingSearch(false);
    }
  };

  const handleGetVectorStats = async () => {
    try {
      const res = await fetch(`${API}/vector/stats`);
      if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);
      const data = await res.json();
      setVectorStats(data);
    } catch (err) {
      console.error("Failed to get vector stats:", err);
      setError(`Failed to get vector database stats.`);
    }
  };



  const tabs = [
    { key: 'home', label: 'Home', icon: Home },
    { key: 'upload', label: 'Upload', icon: Upload },
    { key: 'ask', label: 'Ask', icon: MessageSquare },
    { key: 'simulate', label: 'Simulate', icon: FlaskConical },
    { key: 'vector', label: 'Vector DB', icon: Database },
  ];

  return (
    <div className="space-y-6">
      {/* Navigation Tabs - Hidden on home page */}
      {activeTab !== 'home' && (
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4">
          <div className="flex flex-wrap gap-2">
            {tabs.map(({ key, label, icon: Icon }) => (
              <Tab
                key={key}
                active={activeTab === key}
                onClick={() => setActiveTab(key)}
                icon={Icon}
              >
                {label}
              </Tab>
            ))}
          </div>
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg">
          <span className="block sm:inline">{error}</span>
          <button 
            onClick={() => setError(null)}
            className="float-right text-red-500 hover:text-red-700"
          >
            ×
          </button>
        </div>
      )}

      {/* Content Areas */}
      <div className={activeTab === 'home' ? '' : 'bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6'}>
        {activeTab === 'home' && (
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
                onClick={() => setActiveTab('upload')}
                className="px-6 py-3 bg-blue-600 dark:bg-blue-500 text-white font-semibold rounded-lg hover:bg-blue-700 dark:hover:bg-blue-600 transition"
              >
                Get Started
              </button>
            </div>

            {/* Right Visual - Spline components */}
            <div className="mt-10 lg:mt-0">
              <div className="block dark:hidden">
                <SplineLight />
              </div>
              <div className="hidden dark:block">
                <SplineDark />
              </div>
            </div>
          </div>
        )}

        {activeTab === 'upload' && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">📁 Upload Document</h2>
            <div className="space-y-4">
              <input
                type="file"
                onChange={(e) => setFile(e.target.files[0])}
                className="w-full text-gray-700 dark:text-gray-300 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
              />
              <button
                onClick={handleFileUpload}
                disabled={isLoadingUpload}
                className="w-full py-3 px-6 text-lg font-bold text-white rounded-xl shadow-md bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400"
              >
                {isLoadingUpload ? <LoadingSpinner /> : "Upload"}
              </button>
            </div>
            
            {uploadResult && (
              <div className="mt-6 space-y-4">
                <Section title="Summary" content={uploadResult.summary} />
                <Section title="Document ID" content={uploadResult.doc_id} />
                <Section title="Message" content={uploadResult.message} />
              </div>
            )}
          </div>
        )}

        {activeTab === 'ask' && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">💬 Ask a Question</h2>
            <div className="space-y-4">
              <textarea
                className="w-full border-2 border-gray-200 dark:border-gray-600 rounded-xl p-4 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                rows={5}
                placeholder="Paste context here or upload a document first..."
                value={context}
                onChange={(e) => setContext(e.target.value)}
              />
              <input
                type="text"
                className="w-full border-2 border-gray-200 dark:border-gray-600 rounded-xl p-4 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                placeholder="Type your question here..."
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
              />
              <button
                onClick={handleAsk}
                disabled={isLoadingAsk}
                className="w-full py-3 px-6 text-lg font-bold text-white rounded-xl shadow-md bg-green-600 hover:bg-green-700 disabled:bg-gray-400"
              >
                {isLoadingAsk ? <LoadingSpinner /> : "Ask"}
              </button>
            </div>
            
            {answer && (
              <div className="mt-6">
                <Section title="Answer" content={answer} />
              </div>
            )}
          </div>
        )}

        {activeTab === 'simulate' && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">🧪 Simulate a Scenario</h2>
            <div className="space-y-4">
              <textarea
                className="w-full border-2 border-gray-200 dark:border-gray-600 rounded-xl p-4 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                rows={5}
                placeholder="Paste context here or upload a document first..."
                value={context}
                onChange={(e) => setContext(e.target.value)}
              />
              <input
                type="text"
                className="w-full border-2 border-gray-200 dark:border-gray-600 rounded-xl p-4 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                placeholder="Describe your scenario..."
                value={scenario}
                onChange={(e) => setScenario(e.target.value)}
              />
              <button
                onClick={handleSimulate}
                disabled={isLoadingSimulate}
                className="w-full py-3 px-6 text-lg font-bold text-white rounded-xl shadow-md bg-purple-600 hover:bg-purple-700 disabled:bg-gray-400"
              >
                {isLoadingSimulate ? <LoadingSpinner /> : "Simulate"}
              </button>
            </div>
            
            {simulation && (
              <div className="mt-6">
                <Section title="Simulation Result" content={simulation} />
              </div>
            )}
          </div>
        )}

        {activeTab === 'vector' && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">🔍 Vector Database</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Search Documents</h3>
                <input
                  type="text"
                  className="w-full border-2 border-gray-200 dark:border-gray-600 rounded-xl p-4 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                  placeholder="Enter search query..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
                <button
                  onClick={handleVectorSearch}
                  disabled={isLoadingSearch}
                  className="w-full py-3 px-6 text-lg font-bold text-white rounded-xl shadow-md bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400"
                >
                  {isLoadingSearch ? <LoadingSpinner /> : "Search"}
                </button>
              </div>
              
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Database Stats</h3>
                <button
                  onClick={handleGetVectorStats}
                  className="w-full py-3 px-6 text-lg font-bold text-white rounded-xl shadow-md bg-green-600 hover:bg-green-700"
                >
                  Get Stats
                </button>
                
                {vectorStats && (
                  <div className="bg-gray-100 dark:bg-gray-700 p-4 rounded-lg">
                    <p className="text-sm text-gray-600 dark:text-gray-300">
                      Total Documents: {vectorStats.total_documents}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-300">
                      Storage: {vectorStats.persist_directory}
                    </p>
                  </div>
                )}
              </div>
            </div>
            
            {searchResults.length > 0 && (
              <div className="mt-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Search Results</h3>
                <div className="space-y-4">
                  {searchResults.map((result, index) => (
                    <div key={index} className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                        Similarity: {(1 - result.distance).toFixed(3)}
                      </p>
                      <p className="text-gray-900 dark:text-white">{result.document}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}


      </div>
    </div>
  );
}
