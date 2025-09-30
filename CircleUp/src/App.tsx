import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Home from './pages/Home'
import Layout from './pages/layout'
import Login from './pages/login'
import Signup from './pages/signup'
import UserProfile from './pages/UserProfile'
import CreatePost from './pages/CreatePost'
import EditProfile from './pages/EditProfile'
import Followers from './pages/Followers'
import Following from './pages/Following'
import Chat from './pages/Chat'

function App() {

  return (
    <>
      <BrowserRouter >
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route element={<Layout />}>
            <Route path="/" element={<Home />} />
            <Route path="/profile" element={<UserProfile />} />
            <Route path="/create" element={<CreatePost />} />
            <Route path="/profile/edit" element={<EditProfile />} />
            <Route path="/profile/followers" element={<Followers />} />
            <Route path="/profile/following" element={<Following />} />
            <Route path="/chat" element={<Chat />} />
          </Route>
        </Routes>
      </BrowserRouter >
    </>
  )
}

export default App
