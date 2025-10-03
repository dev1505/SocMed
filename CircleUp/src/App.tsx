import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Chat from './pages/Chat'
import ChatUser from './pages/ChatUser'
import CreatePost from './pages/CreatePost'
import EditProfile from './pages/EditProfile'
import Followers from './pages/Followers'
import Following from './pages/Following'
import Home from './pages/Home'
import Layout from './pages/layout'
import Login from './pages/login'
import Signup from './pages/signup'
import UserProfile from './pages/UserProfile'

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
            <Route path="/chat/user" element={<ChatUser />} />
          </Route>
        </Routes>
      </BrowserRouter >
    </>
  )
}

export default App
