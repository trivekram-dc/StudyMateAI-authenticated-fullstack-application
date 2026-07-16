import { Navigate, Route, Routes } from 'react-router-dom'
import ProtectedRoute from './components/ProtectedRoute'
import Layout from './components/Layout'
import Landing from './pages/Landing'
import AuthPage from './pages/AuthPage'
import Dashboard from './pages/Dashboard'
import Courses from './pages/Courses'
import CourseDetail from './pages/CourseDetail'
import MaterialForm from './pages/MaterialForm'
import StudyAssistant from './pages/StudyAssistant'

const privatePage = (Page) => <ProtectedRoute><Layout><Page /></Layout></ProtectedRoute>
export default function App() { return <Routes><Route path="/" element={<Landing />} /><Route path="/login" element={<AuthPage mode="login" />} /><Route path="/register" element={<AuthPage mode="register" />} /><Route path="/dashboard" element={privatePage(Dashboard)} /><Route path="/courses" element={privatePage(Courses)} /><Route path="/courses/:courseId" element={privatePage(CourseDetail)} /><Route path="/materials/new" element={privatePage(MaterialForm)} /><Route path="/study" element={privatePage(StudyAssistant)} /><Route path="*" element={<Navigate to="/" replace />} /></Routes> }
