
export default function Chat() {
  const users = [1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4];

  return (
    <div className="">
      <div className="flex flex-col w-full h-screen p-5 gap-2">
        {users.map((data, index) => (
          <div
            key={index}
            className="flex justify-around items-center gap-3 rounded py-4 bg-orange-300"
          >
            <div className="flex  items-center gap-3">
              <img
                src="https://picsum.photos/600"
                alt="profile"
                className="w-20 h-20 rounded-full object-cover"
              />
              <span className="text-gray-800 font-medium">Username</span>
            </div>
            <div className="flex gap-3 justify-center items-center">
              <div>
                3 Posts
              </div>
              <div>
                <button
                  className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-5 py-2 rounded hover:from-purple-600 hover:to-pink-600 transition-all duration-300 transform hover:scale-105"
                >Unfollow</button>
              </div>
            </div>
          </div>

        ))}
      </div>
    </div>
  );
}