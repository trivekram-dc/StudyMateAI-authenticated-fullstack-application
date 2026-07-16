import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../lib/api'
import { useAuth } from '../state/AuthContext'

const STARTER_COURSES = [
  { title: 'Introduction to Biology', description: 'Cell structure, genetics, and core biological systems.' },
  { title: 'Cognitive Psychology', description: 'Memory, attention, learning, and decision-making notes.' },
  { title: 'Web Development', description: 'Frontend, backend, and full-stack development study materials.' },
  { title: 'Statistics', description: 'Probability, data analysis, and hypothesis-testing practice.' },
]

export default function Courses() {
  const { accessToken } = useAuth()
  const [courses, setCourses] = useState([])
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [error, setError] = useState('')
  const [addingTemplate, setAddingTemplate] = useState('')
  const load = () => api('/courses', { token: accessToken }).then(data => setCourses(data.courses))
  useEffect(() => { load().catch(err => setError(err.message)) }, [])
  const createCourse = async course => {
    try { await api('/courses', { token: accessToken, method: 'POST', body: JSON.stringify(course) }); await load() }
    catch (err) { setError(err.message) }
  }
  const create = async event => { event.preventDefault(); await createCourse({ title, description }); setTitle(''); setDescription('') }
  const addStarter = async starter => { setAddingTemplate(starter.title); await createCourse(starter); setAddingTemplate('') }
  return <><header className="page-heading"><p className="eyebrow">ORGANIZE YOUR LEARNING</p><h1>Courses</h1><p>Give each class or learning goal a dedicated home.</p></header><div className="two-column"><div><form className="panel" onSubmit={create}><h2>New course</h2><label>Course name<input value={title} onChange={event => setTitle(event.target.value)} required placeholder="e.g. Cognitive Psychology" /></label><label>Description <small>(optional)</small><textarea value={description} onChange={event => setDescription(event.target.value)} placeholder="What are you learning?" /></label>{error && <p className="error">{error}</p>}<button className="button full">Create course</button></form><section className="panel"><h2>Course starters</h2><p className="muted">Add a starter course to your own workspace.</p>{STARTER_COURSES.map(starter => <button className="secondary-button full" type="button" key={starter.title} disabled={addingTemplate === starter.title} onClick={() => addStarter(starter)}>{addingTemplate === starter.title ? 'Adding…' : `Add ${starter.title}`}</button>)}</section></div><section className="course-list">{courses.length ? courses.map(course => <Link key={course.id} to={`/courses/${course.id}`} className="list-card"><div><h2>{course.title}</h2><p>{course.description || 'No description yet.'}</p></div><span>{course.materialCount} items →</span></Link>) : <div className="empty compact"><p>No courses yet — choose a course starter or create your own.</p></div>}</section></div></>
}
