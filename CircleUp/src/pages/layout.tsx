import axios from 'axios'
import { useEffect, useState } from 'react'
import { Navigate, Outlet } from 'react-router-dom'
import SearchBar from '../components/searchBar'
import Sidebar from '../components/sidebar'
import { django_app_backend_url } from '../defaults'

export default function Layout() {
    const [userCreds, setUserCreds] = useState({ isLoggedIn: true })

    useEffect(() => {
        (
            async () => {
                try {
                    const response = await axios.get(django_app_backend_url + "/auth", { withCredentials: true })
                    console.log(response)
                } catch (error) {
                    setUserCreds({ ...userCreds, isLoggedIn: false })
                    console.log(error)
                }
            }
        )()
    }, [])

    return (
        <div>
            <Sidebar />
            <div
                className="bg-orange-100 fixed md:left-1/12 md:w-11/12 w-full md:h-full h-11/12 pt-3 px-4 overflow-y-auto"
            >
                <SearchBar />
                {userCreds.isLoggedIn ? <Outlet /> : <Navigate to="/login" replace={true} />}
            </div>
        </div>
    )
}
