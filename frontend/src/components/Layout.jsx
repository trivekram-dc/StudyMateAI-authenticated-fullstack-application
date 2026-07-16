import { Link, NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../state/AuthContext'
import { api } from '../lib/api'

export default function Layout({ children }) {
  const { user, accessToken, logout } = useAuth(); const navigate = useNavigate()
  const leave = async () => { try { await api('/auth/logout', { token: accessToken, method: 'POST' }) } catch { /* Clear the local session even if the server is unavailable. */ } finally { logout(); navigate('/') } }
  return <div className="app-shell"><aside><Link className="brand" to="/dashboard"><span>✦</span> StudyMate</Link><nav><NavLink to="/dashboard">Overview</NavLink><NavLink to="/courses">Courses</NavLink><NavLink to="/materials/new">Add material</NavLink><NavLink to="/study">Study assistant</NavLink></nav><div className="profile"><div><strong>{user?.username}</strong><small>{user?.email}</small></div><button className="text-button" onClick={leave}>Sign out</button></div></aside><section className="workspace">{children}</section></div>
}
