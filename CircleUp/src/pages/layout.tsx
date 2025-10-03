import { Outlet } from 'react-router-dom';
import Sidebar from '../components/sidebar';

export default function Layout() {

    return (
        <div>
            <Sidebar />
            <div
                className="bg-orange-100 fixed md:left-1/12 md:w-11/12 w-full md:h-full h-11/12 pt-3 px-4 overflow-y-auto"
            >
                <Outlet />
            </div>
        </div>
    )
}
