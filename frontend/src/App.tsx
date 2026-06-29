import { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { atomDark } from 'react-syntax-highlighter/dist/cjs/styles/prism';

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [template, setTemplate] = useState<'standard' | 'physics' | 'chemistry'>('standard');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<any>(null);

  const onDrop = (acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
      setError(null);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png']
    },
    maxFiles: 1,
  });

  const handleConvert = async () => {
    if (!file) return;
    
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('template', template);
      
      const response = await axios.post('/api/convert', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      
      setResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = async () => {
    if (!result) return;
    
    try {
      const response = await axios.get('/api/download/' + result.task_id, {
        responseType: 'blob',
      });
      
      const url = window.URL.createObjectURL(response.data);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'latex_' + result.task_id + '.zip';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      setError('Failed to download');
    }
  };

  const handleReset = () => {
    setFile(null);
    setResult(null);
    setError(null);
  };

  return (
    <div className="container">
      <h1>PDF/Image to LaTeX Converter</h1>
      
      <div className="card">
        <h2>Upload your file</h2>
        <div {...getRootProps()} className={'upload-zone ' + (isDragActive ? 'active' : '')}>
          <input {...getInputProps()} />
          <p>{isDragActive ? 'Drop the file here...' : 'Drag & drop a PDF, JPG, or PNG file here, or click to select'}</p>
        </div>
        
        {file && (
          <div>
            <p>Selected: <strong>{file.name}</strong> ({Math.round(file.size / 1024)} KB)</p>
            <div style={{ margin: '1rem 0' }}>
              <label htmlFor="template-select" style={{ display: 'block', marginBottom: '0.5rem' }}>Template:</label>
              <select
                id="template-select"
                value={template}
                onChange={(e) => setTemplate(e.target.value as 'standard' | 'physics' | 'chemistry')}
                className="select"
              >
                <option value="standard">Standard (Generic)</option>
                <option value="physics">Physics (circuitikz, pgfplots)</option>
                <option value="chemistry">Chemistry (chemfig, mhchem)</option>
              </select>
            </div>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button
                onClick={handleConvert}
                disabled={isLoading}
                className="button button-primary"
              >
                {isLoading ? 'Converting...' : 'Convert to LaTeX'}
              </button>
              <button
                onClick={handleReset}
                disabled={isLoading}
                className="button button-secondary"
              >
                Reset
              </button>
            </div>
          </div>
        )}
        
        {error && (
          <div className="error">
            Error: {error}
          </div>
        )}
      </div>

      {result && (
        <div className="card">
          <h2>Conversion Complete</h2>
          <div style={{ marginBottom: '1rem' }}>
            <p><strong>Source:</strong> {result.metadata.source_file}</p>
            <p><strong>Template:</strong> {result.metadata.template_used}</p>
            <p><strong>Images extracted:</strong> {result.images.length}</p>
            <p><strong>Timestamp:</strong> {new Date(result.metadata.timestamp).toLocaleString()}</p>
          </div>

          {result.warnings.length > 0 && (
            <div className="warning">
              {result.warnings.length} warning(s):
              <ul style={{ marginLeft: '1.5rem' }}>
                {result.warnings.map((warning: string, index: number) => (
                  <li key={index}>{warning}</li>
                ))}
              </ul>
            </div>
          )}

          <h3>LaTeX Preview (first 50 lines):</h3>
          <div className="latex-preview">
            <SyntaxHighlighter language="latex" style={atomDark}>
              {result.preview}
            </SyntaxHighlighter>
          </div>

          <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1rem' }}>
            <button
              onClick={handleDownload}
              className="button button-primary"
            >
              Download ZIP
            </button>
            <button
              onClick={handleReset}
              className="button button-secondary"
            >
              New Conversion
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
