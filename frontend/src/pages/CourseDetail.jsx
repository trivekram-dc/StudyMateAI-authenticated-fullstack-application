import { Link, useNavigate, useParams } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { api } from '../lib/api'
import { useAuth } from '../state/AuthContext'

export default function CourseDetail() {
  const { courseId } = useParams()
  const { accessToken } = useAuth()
  const navigate = useNavigate()
  const [course, setCourse] = useState(null)
  const [editing, setEditing] = useState(false)
  const [form, setForm] = useState({ title: '', description: '' })
  const [error, setError] = useState('')
  const load = () => api(`/courses/${courseId}`, { token: accessToken }).then(({ course: next }) => { setCourse(next); setForm({ title: next.title, description: next.description }) }).catch(err => setError(err.message))
  useEffect(() => { load() }, [courseId])
  const save = async event => { event.preventDefault(); try { await api(`/courses/${courseId}`, { token: accessToken, method: 'PUT', body: JSON.stringify(form) }); setEditing(false); load() } catch (err) { setError(err.message) } }
  const removeCourse = async () => { if (!window.confirm('Delete this course and all of its materials?')) return; try { await api(`/courses/${courseId}`, { token: accessToken, method: 'DELETE' }); navigate('/courses') } catch (err) { setError(err.message) } }
  const removeMaterial = async id => { if (!window.confirm('Delete this study material?')) return; try { await api(`/materials/${id}`, { token: accessToken, method: 'DELETE' }); load() } catch (err) { setError(err.message) } }
  if (!course) return <p>{error || 'Loading course…'}</p>
  return <><header className="page-heading split"><div><p className="eyebrow">COURSE</p>{editing ? <form className="inline-editor" onSubmit={save}><input value={form.title} onChange={e => setForm({ ...form, title: e.target.value })} required /><textarea value={form.description} onChange={e => setForm({ ...form, description: e.target.value })} placeholder="Course description" /><button className="button">Save changes</button><button type="button" className="secondary-button" onClick={() => setEditing(false)}>Cancel</button></form> : <><h1>{course.title}</h1><p>{course.description || 'No description yet.'}</p></>}</div><div className="heading-actions"><Link className="button" to={`/materials/new?courseId=${course.id}`}>Add material</Link><button className="secondary-button" onClick={() => setEditing(true)}>Edit course</button><button className="danger-button" onClick={removeCourse}>Delete course</button></div></header>{error && <p className="error">{error}</p>}<section className="section-header"><h2>Study materials</h2><span>{course.materials.length} total</span></section>{course.materials.length ? <div className="material-list">{course.materials.map(material => <article key={material.id} className="list-card"><div><span className="tag">{material.materialType}</span><h2>{material.title}</h2><p>{material.content.slice(0, 180)}{material.content.length > 180 ? '…' : ''}</p></div><div className="card-actions"><Link className="quiet-link" to={`/study?materialId=${material.id}`}>Study this →</Link><button className="text-button delete" onClick={() => removeMaterial(material.id)}>Delete</button></div></article>)}</div> : <div className="empty"><h2>No material yet.</h2><p>Add a set of notes or a reading to start studying with this course.</p><Link className="button" to={`/materials/new?courseId=${course.id}`}>Add material</Link></div>}</>
}
