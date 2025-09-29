export default function SearchBar() {
    return (
        <div>
            <form>
                <input
                    type="text"
                    name="searchbar"
                    id="searchbar"
                    className="rounded-md bg-white mt-2 p-2 w-full focus:outline-2 outline-orange-400"
                    placeholder="Search Here"
                />
            </form>
        </div>
    )
}
