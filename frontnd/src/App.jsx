import React, { useState } from "react";
import { Upload, MessageSquare, FlaskConical, X, Home } from "lucide-react";

// The API endpoint remains the same.
const API = "http://127.0.0.1:8000";

// Loading spinner component
const LoadingSpinner = () => (
  <div className="flex justify-center items-center py-4">
    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white"></div>
  </div>
);

// Custom modal for displaying errors or messages
const ErrorModal = ({ message, onClose }) => (
  <div className="fixed inset-0 z-50 flex items-center justify-center bg-gray-900 bg-opacity-50">
    <div className="bg-white p-6 rounded-2xl shadow-xl max-w-sm w-full relative transform transition-all duration-300 scale-100">
      <button onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition-colors">
        <X size={20} />
      </button>
      <div className="flex items-center space-x-3 mb-4">
        <div className="flex-shrink-0 bg-red-100 p-2 rounded-full">
          <X className="text-red-500" size={24} />
        </div>
        <h3 className="text-xl font-bold text-red-600">Error</h3>
      </div>
      <p className="text-gray-700">{message}</p>
    </div>
  </div>
);

// Section component for styled cards
// It now supports rendering both paragraphs and lists
const Section = ({ title, content }) => (
  <div className="bg-white border border-gray-200 p-6 rounded-2xl shadow-lg transform hover:scale-105 transition-transform duration-300">
    <h3 className="text-xl font-semibold mb-3 text-indigo-700">{title}</h3>
    <div className="space-y-2 text-gray-700">
      {content.map((block, index) => {
        if (block.type === 'paragraph') {
          return <p key={index}>{block.text}</p>;
        } else if (block.type === 'list') {
          return (
            <ul key={index} className="list-disc list-inside">
              {block.items.map((item, i) => (
                <li key={i}>{item}</li>
              ))}
            </ul>
          );
        }
        return null;
      })}
    </div>
  </div>
);

// Advanced parser: extracts sections, paragraphs, and bullet points from markdown
const parseMarkdownToSections = (text = "") => {
  const sections = [];
  const lines = text.split(/\r?\n/);
  let currentSection = { title: "Result", content: [] };
  let currentList = null;

  for (const line of lines) {
    const trimmedLine = line.trim();
    if (trimmedLine.length === 0) {
      if (currentList) {
        currentSection.content.push({ type: 'list', items: currentList });
        currentList = null;
      }
      continue;
    }

    // Check for a new section title enclosed in double asterisks
    if (trimmedLine.startsWith('**') && trimmedLine.endsWith('**')) {
      if (currentList) {
        currentSection.content.push({ type: 'list', items: currentList });
        currentList = null;
      }
      if (currentSection.content.length > 0) {
        sections.push(currentSection);
      }
      const title = trimmedLine.slice(2, -2).trim();
      currentSection = { title, content: [] };
    } 
    // Check for a bullet point
    else if (trimmedLine.startsWith('*')) {
      if (!currentList) {
        currentList = [];
      }
      const point = trimmedLine.replace(/^\*+\s*/, '').trim();
      if (point) {
        currentList.push(point);
      }
    } 
    // Handle plain text as a new paragraph
    else {
      if (currentList) {
        currentSection.content.push({ type: 'list', items: currentList });
        currentList = null;
      }
      currentSection.content.push({ type: 'paragraph', text: trimmedLine });
    }
  }

  // Push any remaining list content
  if (currentList) {
    currentSection.content.push({ type: 'list', items: currentList });
  }
  // Push the final section if it has content
  if (currentSection.content.length > 0) {
    sections.push(currentSection);
  }

  // Fallback for cases with no structured markdown
  if (sections.length === 0 && text.trim().length > 0) {
    return [{ title: "Result", content: [{ type: 'paragraph', text: text.trim() }] }];
  }
  
  return sections;
};

// Reusable FeatureCard component for the homepage
const FeatureCard = ({ title, description, icon: Icon, onClick, color }) => (
  <div onClick={onClick} className={`p-6 bg-white rounded-3xl shadow-xl border-t-4 ${color} transform transition-all duration-300 hover:scale-105 cursor-pointer`}>
    <div className="flex items-center space-x-4 mb-4">
      <div className={`p-3 rounded-full bg-opacity-20 ${color.replace('border-t-4 ', 'bg-')}`}>
        <Icon size={28} className={color.replace('border-t-4 ', 'text-')} />
      </div>
      <h3 className="text-2xl font-bold text-gray-800">{title}</h3>
    </div>
    <p className="text-gray-600">{description}</p>
  </div>
);

export default function App() {
  // Main state for the application. The default page is now "home".
  const [page, setPage] = useState("home");
  const [file, setFile] = useState(null);
  const [uploadResult, setUploadResult] = useState(null);
  const [context, setContext] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [scenario, setScenario] = useState("");
  const [simulation, setSimulation] = useState("");
  
  // State for loading and error handling
  const [isLoadingUpload, setIsLoadingUpload] = useState(false);
  const [isLoadingAsk, setIsLoadingAsk] = useState(false);
  const [isLoadingSimulate, setIsLoadingSimulate] = useState(false);
  const [error, setError] = useState(null);

  // Handlers for API interactions
  const handleFileUpload = async () => {
    if (!file) {
      setError("Please choose a file to upload.");
      return;
    }

    setIsLoadingUpload(true);
    setError(null); // Clear previous errors
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

  // Parse results for display
  const uploadSections = uploadResult?.summary
    ? parseMarkdownToSections(uploadResult.summary)
    : [];
  const askSections = answer
    ? parseMarkdownToSections(answer)
    : [];
  const simulateSections = simulation
    ? parseMarkdownToSections(simulation)
    : [];

  // Render the main application UI
  return (
    <div className="min-h-screen bg-gray-50 flex font-sans text-gray-800">
      {/* Sidebar */}
      <div className="w-64 bg-white shadow-xl p-6 space-y-6 transition-all duration-300">
        <h1 className="text-3xl font-extrabold text-blue-800 mb-6 tracking-wide">Parse AI</h1>
        <nav className="space-y-4">
          {[
            { key: "home", label: "Home", icon: Home },
            { key: "upload", label: "Upload", icon: Upload },
            { key: "ask", label: "Ask", icon: MessageSquare },
            { key: "simulate", label: "Simulate", icon: FlaskConical },
          ].map(({ key, label, icon: Icon }) => (
            <button
              key={key}
              onClick={() => setPage(key)}
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-200 
                ${page === key ? "bg-blue-600 text-white shadow-md transform scale-105" : "text-gray-600 hover:bg-gray-100"} 
                focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50`}
            >
              <Icon size={20} />
              <span className="font-medium">{label}</span>
            </button>
          ))}
        </nav>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 p-10 overflow-auto">
        <div className="max-w-4xl mx-auto">
          {page === "home" && (
            <div className="space-y-10">
              <div className="bg-white p-8 rounded-3xl shadow-2xl text-center">
                <h2 className="text-5xl font-bold text-gray-800 tracking-tight mb-4">Welcome to ClaimBot</h2>
                <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
                  Your professional assistant for understanding and analyzing insurance claims documents.
                </p>
                <div className="flex flex-wrap justify-center gap-6">
                  <button
                    onClick={() => setPage("upload")}
                    className="flex items-center space-x-2 py-3 px-6 text-lg font-bold text-white rounded-xl shadow-lg transform transition-all duration-300 bg-gradient-to-r from-blue-500 to-blue-700 hover:from-blue-600 hover:to-blue-800 hover:scale-105"
                  >
                    <Upload size={24} />
                    <span>Get Started - Upload</span>
                  </button>
                  <button
                    onClick={() => setPage("ask")}
                    className="flex items-center space-x-2 py-3 px-6 text-lg font-bold text-white rounded-xl shadow-lg transform transition-all duration-300 bg-gradient-to-r from-indigo-500 to-indigo-700 hover:from-indigo-600 hover:to-indigo-800 hover:scale-105"
                  >
                    <MessageSquare size={24} />
                    <span>Ask a Question</span>
                  </button>
                  <button
                    onClick={() => setPage("simulate")}
                    className="flex items-center space-x-2 py-3 px-6 text-lg font-bold text-white rounded-xl shadow-lg transform transition-all duration-300 bg-gradient-to-r from-purple-500 to-purple-700 hover:from-purple-600 hover:to-purple-800 hover:scale-105"
                  >
                    <FlaskConical size={24} />
                    <span>Simulate a Scenario</span>
                  </button>
                </div>
              </div>
              
              {/* Features Section */}
              <div className="mt-12">
                <h2 className="text-4xl font-bold text-center text-gray-800 mb-8">Features</h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                  <FeatureCard
                    title="Document Upload"
                    description="Securely upload your insurance claims documents to get a quick and accurate summary."
                    icon={Upload}
                    onClick={() => setPage('upload')}
                    color="border-t-4 border-blue-500"
                  />
                  <FeatureCard
                    title="Ask Questions"
                    description="Get instant answers to specific questions about the documents you've uploaded."
                    icon={MessageSquare}
                    onClick={() => setPage('ask')}
                    color="border-t-4 border-indigo-500"
                  />
                  <FeatureCard
                    title="Simulate Scenarios"
                    description="Run simulations on your claims data to predict outcomes and explore possibilities."
                    icon={FlaskConical}
                    onClick={() => setPage('simulate')}
                    color="border-t-4 border-purple-500"
                  />
                </div>
              </div>
            </div>
          )}

          {page === "upload" && (
            <div className="bg-white p-8 rounded-3xl shadow-2xl">
              <h2 className="text-3xl font-bold mb-6 text-gray-800">📁 Upload Document</h2>
              <div className="space-y-6">
                <input
                  type="file"
                  onChange={(e) => setFile(e.target.files[0])}
                  className="w-full text-gray-700 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 transition duration-200"
                />
                <button
                  onClick={handleFileUpload}
                  className={`w-full py-3 px-6 text-lg font-bold text-white rounded-xl shadow-md transform transition-all duration-300 
                  ${isLoadingUpload ? "bg-gray-400 cursor-not-allowed" : "bg-gradient-to-r from-blue-500 to-blue-700 hover:from-blue-600 hover:to-blue-800 hover:scale-105"}`}
                  disabled={isLoadingUpload}
                >
                  {isLoadingUpload ? <LoadingSpinner /> : "Upload"}
                </button>
              </div>
              <div className="mt-8 space-y-6">
                {uploadSections.map((sec, i) => (
                  <Section key={i} title={sec.title} content={sec.content} />
                ))}
              </div>
            </div>
          )}

          {page === "ask" && (
            <div className="bg-white p-8 rounded-3xl shadow-2xl">
              <h2 className="text-3xl font-bold mb-6 text-gray-800">💬 Ask a Question</h2>
              <div className="space-y-6">
                <textarea
                  className="w-full border-2 border-gray-200 rounded-xl p-4 transition-all duration-300 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 resize-none shadow-sm"
                  rows={5}
                  placeholder="Paste context here or upload a document first..."
                  value={context}
                  onChange={(e) => setContext(e.target.value)}
                />
                <input
                  type="text"
                  className="w-full border-2 border-gray-200 rounded-xl p-4 transition-all duration-300 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 shadow-sm"
                  placeholder="Type your question here..."
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                />
                <button
                  onClick={handleAsk}
                  className={`w-full py-3 px-6 text-lg font-bold text-white rounded-xl shadow-md transform transition-all duration-300 
                  ${isLoadingAsk ? "bg-gray-400 cursor-not-allowed" : "bg-gradient-to-r from-indigo-500 to-indigo-700 hover:from-indigo-600 hover:to-indigo-800 hover:scale-105"}`}
                  disabled={isLoadingAsk}
                >
                  {isLoadingAsk ? <LoadingSpinner /> : "Ask"}
                </button>
              </div>
              <div className="mt-8 space-y-6">
                {askSections.map((sec, i) => (
                  <Section key={i} title={sec.title} content={sec.content} />
                ))}
              </div>
            </div>
          )}

          {page === "simulate" && (
            <div className="bg-white p-8 rounded-3xl shadow-2xl">
              <h2 className="text-3xl font-bold mb-6 text-gray-800">🧪 Simulate a Scenario</h2>
              <div className="space-y-6">
                <textarea
                  className="w-full border-2 border-gray-200 rounded-xl p-4 transition-all duration-300 focus:border-purple-500 focus:ring-1 focus:ring-purple-500 resize-none shadow-sm"
                  rows={5}
                  placeholder="Paste context here or upload a document first..."
                  value={context}
                  onChange={(e) => setContext(e.target.value)}
                />
                <input
                  type="text"
                  className="w-full border-2 border-gray-200 rounded-xl p-4 transition-all duration-300 focus:border-purple-500 focus:ring-1 focus:ring-purple-500 shadow-sm"
                  placeholder="Describe your scenario..."
                  value={scenario}
                  onChange={(e) => setScenario(e.target.value)}
                />
                <button
                  onClick={handleSimulate}
                  className={`w-full py-3 px-6 text-lg font-bold text-white rounded-xl shadow-md transform transition-all duration-300 
                  ${isLoadingSimulate ? "bg-gray-400 cursor-not-allowed" : "bg-gradient-to-r from-purple-500 to-purple-700 hover:from-purple-600 hover:to-purple-800 hover:scale-105"}`}
                  disabled={isLoadingSimulate}
                >
                  {isLoadingSimulate ? <LoadingSpinner /> : "Simulate"}
                </button>
              </div>
              <div className="mt-8 space-y-6">
                {simulateSections.map((sec, i) => (
                  <Section key={i} title={sec.title} content={sec.content} />
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
      {error && <ErrorModal message={error} onClose={() => setError(null)} />}
    </div>
  );
}
