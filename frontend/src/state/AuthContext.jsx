import { createContext, useContext, useEffect, useState } from 'react'
import { api } from '../lib/api'

const AuthContext = createContext(null)
const STORAGE_KEY = 'studymate-session'

export function AuthProvider({ children }) {
  const [session, setSession] = useState(() => JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null'))
  const [loading, setLoading] = useState(true)
  useEffect(() => {
    if (!session?.accessToken) return setLoading(false)
    api('/auth/me', { token: session.accessToken }).then(({ user }) => setSession(current => ({ ...current, user }))).catch(() => localStorage.removeItem(STORAGE_KEY)).finally(() => setLoading(false))
  }, [])
  const authenticate = (next) => { localStorage.setItem(STORAGE_KEY, JSON.stringify(next)); setSession(next) }
  const logout = () => { localStorage.removeItem(STORAGE_KEY); setSession(null) }
  return <AuthContext.Provider value={{ ...session, loading, authenticate, logout }}>{children}</AuthContext.Provider>
}
export const useAuth = () => useContext(AuthContext)
