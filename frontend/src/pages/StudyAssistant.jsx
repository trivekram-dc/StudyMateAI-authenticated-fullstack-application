import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { api } from '../lib/api'
import { useAuth } from '../state/AuthContext'

export default function StudyAssistant() {
  const [params] = useSearchParams(); const { accessToken } = useAuth()
  const [materials, setMaterials] = useState([]); const [materialId, setMaterialId] = useState(params.get('materialId') || '')
  const [question, setQuestion] = useState(''); const [result, setResult] = useState(null); const [busy, setBusy] = useState(false); const [error, setError] = useState('')
  useEffect(() => { api('/materials', { token: accessToken }).then(data => setMaterials(data.materials)).catch(err => setError(err.message)) }, [])
  const run = async action => {
    setBusy(true); setError('')
    try {
      const endpoint = action === 'ask' ? '/ai/ask' : action === 'summary' ? '/ai/summarize' : '/ai/quiz'
      const body = action === 'ask' ? { question, ...(materialId ? { materialId: Number(materialId) } : {}) } : { materialId: Number(materialId) }
      if (action !== 'ask' && !materialId) throw new Error('Choose a study material first.')
      setResult({ action, ...(await api(endpoint, { token: accessToken, method: 'POST', body: JSON.stringify(body) })) })
    } catch (err) { setError(err.message) } finally { setBusy(false) }
  }
  return <><header className="page-heading"><p className="eyebrow">SOURCE-BACKED STUDYING</p><h1>Study assistant</h1><p>Answers are grounded in the material you save here.</p></header><section className="assistant"><div className="assistant-controls"><label>Focus material <small>(optional for questions)</small><select value={materialId} onChange={e => setMaterialId(e.target.value)}><option value="">Search all my materials</option>{materials.map(material => <option value={material.id} key={material.id}>{material.title}</option>)}</select></label><label>Ask a question<textarea value={question} onChange={e => setQuestion(e.target.value)} placeholder="What would you like to understand?" /></label><div className="button-row"><button className="button" disabled={busy} onClick={() => run('ask')}>Ask materials</button><button className="secondary-button" disabled={busy} onClick={() => run('summary')}>Summarize</button><button className="secondary-button" disabled={busy} onClick={() => run('quiz')}>Make quiz</button></div>{error && <p className="error">{error}</p>}</div><div className="result-panel">{busy ? <p>Finding the relevant passages…</p> : result ? <Result result={result} /> : <div className="result-empty"><span>✦</span><h2>Ready when you are.</h2><p>Ask a question, create a summary, or turn a material into practice questions.</p></div>}</div></section></>
}

function Result({ result }) {
  return <div><p className="eyebrow">{result.action === 'quiz' ? 'PRACTICE QUESTIONS' : 'RESPONSE'}{result.mode === 'local-fallback' ? ' · LOCAL STUDY MODE' : ''}</p>{result.answer && <p className="answer">{result.answer}</p>}{result.questions?.map((item, index) => <article className="quiz-question" key={index}><strong>{index + 1}. {item.question}</strong><details><summary>Show answer</summary><p><b>{item.answer}</b> — {item.explanation}</p></details></article>)}<h3>Sources used</h3>{result.sources?.length ? result.sources.map((source, index) => <article className="source" key={index}><strong>{source.materialTitle}</strong><p>{source.excerpt}</p></article>) : <p className="muted">No relevant source passages were found.</p>}</div>
}
