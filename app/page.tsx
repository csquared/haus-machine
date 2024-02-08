import { useState } from 'react'

export default function Home() {
  const [isGenerating, setIsGenerating] = useState(false);
  const [audioSrc, setAudioSrc] = useState('');

  const generateBeat = async () => { 
    const generateResponse = await fetch('/api/v1/gen_audio', { method: 'POST' });
    const { id } = await generateResponse.json();
    console.log(id);

    setIsGenerating(true);

    // Poll the /api/v1/gen_audio_progress endpoint to check the progress
    const checkProgress = () => {
      fetch(`/api/v1/gen_audio_progress?id=${id}`)
        .then((response) => response.json())
        .then((data) => {
          console.log(data)
          const { state } = data;
          if (state === 'PENDING') {
            setTimeout(checkProgress, 1000); // Poll every second
          } else {
            const { result } = data;
            setAudioSrc(result); // Set the source of the audio player to the generated audio URL
            setIsGenerating(false);
          }
        })
        .catch((error) => {
          console.error('Error fetching progress:', error);
          setIsGenerating(false); // In case of error, stop generating
        });
    };

    checkProgress();
  }
    
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24 bg-[url('/background.webp')] bg-cover">
      <div className="text-center">
        <h1 className="text-5xl text-white font-bold mb-6">Haus Machine</h1>
        <button
          onClick={generateBeat}
          disabled={isGenerating}
          className={`text-white font-bold py-2 px-4 rounded-lg transition duration-300 ${isGenerating ? 'animate-pulse bg-blue-400' : 'bg-blue-500 hover:bg-blue-600'}`}
        >
          {isGenerating ? 'Generating...' : 'Generate Beat'}
        </button>
        {(!isGenerating && audioSrc) && <div className="p-4"> <audio controls loop src={audioSrc} /> </div>}
      </div>
    </main>
  )
}