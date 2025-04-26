import { useState } from 'react'
import axios from 'axios'

function App() {
  const [file, setFile] = useState(null)
  const [uploadedImageURL, setUploadedImageURL] = useState(null)
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)

    setLoading(true)
    const res = await axios.post('http://localhost:5000/api/search', formData)
    setResults(res.data)
    setLoading(false)
  }

  const handleFileChange = (e) => {
    const selected = e.target.files[0]
    if (selected) {
      setFile(selected)
      setUploadedImageURL(URL.createObjectURL(selected))
    }
  }

  return (
    <div className="min-h-screen bg-neutral-100 font-sans text-gray-900 px-6 py-10">
      <h1 className="text-3xl font-semibold text-center mb-6">Mercari Fit Pic Search</h1>

      <form onSubmit={handleSubmit} className="flex flex-col items-center gap-4 mb-10">
        <label className="cursor-pointer bg-black text-white px-5 py-2 rounded hover:bg-neutral-800 transition">
          Add A Pic
          <input type="file" onChange={handleFileChange} className="hidden" />
        </label>
        <button
          type="submit"
          className="px-6 py-2 bg-black text-white rounded hover:bg-neutral-800 transition"
        >
          Search
        </button>
      </form>

      {uploadedImageURL && (
        <div className="flex justify-center mb-10">
          <img
            src={uploadedImageURL}
            alt="Uploaded Fit Pic"
            className="max-h-96 max-w-xs object-contain rounded"
          />
        </div>
      )}

      {loading ? (
        <p className="text-center text-lg text-gray-600">Searching...</p>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6 max-w-7xl mx-auto">
          {results.map((item, index) => (
            <div key={index} className="bg-white p-4 shadow rounded">
              <img
                src={`http://localhost:5000/images/${item.filename}`}
                alt={item.title}
                className="w-full h-64 object-cover rounded"
              />
              <h2 className="mt-3 text-sm font-medium">{item.title}</h2>
              <p className="text-xs text-gray-500">{item.price}</p>

              {/* Vibe Match */}
              <div className="mt-2 text-xs text-gray-500">Vibe Match</div>
              <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden mt-1">
                <div
                  className="h-full bg-yellow-500"
                  style={{
                    width: `${Math.round(item.similarity * 100)}%`
                  }}
                />
              </div>
              <p className="text-[10px] text-right text-gray-400 mt-1">
                {Math.round(item.similarity * 100)}%
              </p>

              <a
                href={item.link}
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-blue-600 hover:underline mt-2 block"
              >
                View on Mercari
              </a>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default App
