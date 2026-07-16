import { Navigate } from 'react-router-dom'
import { useAuth } from '../state/AuthContext'

export default function ProtectedRoute({ children }) {
  const { accessToken, loading } = useAuth()
  if (loading) return <main className="centered">Loading your study space…</main>
  return accessToken ? children : <Navigate to="/login" replace />
}
