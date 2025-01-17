# NodeEasyIPC
This is a fork of the [NodeEasyIPC Module](https://github.com/Winexcel/node-easy-ipc). I added a Prebuild for Windows and added a install script.
I forked it because the original didnt worked here.

Easy IPC addon implementation for Windows which allow to use messages, filemapping, mapping/shared memory, mutex, threads.

# Installation

You will need to have visual studio installed on your machine to build! I've only tested with VS 2017 Community, but it will probably work with other versions (No garunteees!). I know it will not work with VS 2012 or earlier, as I used a lot of C++ 11 features in the code.

It should install like any other package, and build the native components automatically:


`npm install @fynnix/node-easy-ipc`

**This library is windows only**. If you want to run your app on other platforms, you can make it an optional install:

`npm install --save-optional @fynnix/node-easy-ipc`

You will then have to deal with the package not being available on other systems in your code. You should look at mmap-io or node-mmap for that.

# How to use

You should probably be familiar with how to use the Win32 file mapping and mutex API's before using this. It's basically just a wrapper around these.

To create a file mapping object:

```js
const NodeIPC = require('node-easy-ipc');
const map = new NodeIPC.FileMapping();

map.createMapping(
    'file.txt',        // Name of file (Can be null if you just want shared memory). If the file does not exist, it will be created.
    'my_mapped_file',  // Shared memory name (Cannot be null).
    20);               // Mapping size - How many bytes of the file to map into memory, or how large of a shared memory location to create.

buffer = Buffer.alloc(20)
map.readInto(
    0,         // What byte offset to start reading from
    20,        // How many bytes to read
    buffer);   // A buffer object to read into

console.log(buffer.ToString('utf8'));
```

#API
## `IPC`
Main interprocess communication interface.
#### `getPID`
Returns pid of current process.

#### `getMainThreadId`
Returns thread id of current Node.js instance.

#### `getMessageThreadId`
Returns thread id of current IPC instance.

#### `waitThread`
Waits while current thread terminates.

#### `on`
Messages listener from other threads.
```js
ipc.on('message', async (data) => {
    console.log(data);
});
```

#### `send` 
Sends message to another thread.

## `FileMapping`

FileMapping objects are used to manage file mappings and shared memory. Windows treats these two uses as nearly identical.

#### `new FileMapping()`

Constructs a new file mapping. You either need to call `createMapping` or `openMapping` to use it, until then it is just empty.

#### `createMapping(file, name, size)`

Creates a new file mapping.

`file` - The name of the file to map into memory. Can be `null` to just create shared memory.

`name` - The name of the shared memory location to make (For interprocess communication).

`size` - How large the memory location should be.

Returns nothing.

#### `openMapping(name, size)`

Opens an existing file mapping.

`name` - The name of the shared memory location/file mapping to open

`size` - The size of the memory location. Should be less than or equal to the size passed into `createMapping`.

Returns nothing.

#### `closeMapping()`

Closes the mapping. `writeBuffer` and `readInto` will no longer work once you do this. You should always call this when you are done with the file mapping. You can re-open the mapping after it is closed by calling `createMapping` or `openMapping`.

Returns nothing.

#### `writeBuffer(buffer, destOffset, srcOffset, length)`

Write a buffer into the file mapping

`buffer` - The buffer to write to the file mapping/shared memory.

`destOffset` - Where to start writing in the destination (The file mapping)

`srcOffset` - Where to start reading in the source (The buffer)

`length` - How many bytes to read from the buffer into the destination. This is not validated - Make sure you don't read off the end of the buffer or write off the end of the destination~

Returns nothing

#### `readInto(offset, length, buffer)`

Reads data from the file mapping into a buffer

`offset` The byte offset to start reading from in the file mapping

`length` The number of bytes to read

`buffer` The buffer to read into

Returns nothing

## `Mutex`

I couldn't find a good interprocess mutex library for NodeJS on Windows (Microsoft has one but it doesn't support named Mutexes).

#### `new Mutex`

Just like `new FileMap`. Doesn't actually initialize the object - you need to call `create` or `open` to do that.

#### `create(name)`

Creates a named mutex

`name` - The name to give the mutex

Returns nothing

#### `open(name)`

Opens a named mutex that was previously created in another process

`name` - The name of the mutex to open

Returns nothing

#### `close()`

Closes the handle to this mutex. Always call this before ending your process.

#### `wait([time])`

Acquires this mutex

`time` - Optional. How long to wait for the lock to be granted. Defaults to `INFINITE`.

Returns `WAIT_ABANDONED`, `WAIT_OBJECT_0`, or `WAIT_TIMEOUT`. `WAIT_OBJECT_0` means the lock was granted to your process. `WAIT_TIMEOUT` means that the time you passed in had elapsed without the lock being granted. `WAIT_ABANDONED` means the mutex was abandoned.

#### `waitMultiple(mutexList, waitForAll, time)`

Waits for multiple mutexes

`mutexList` - A list of all the mutexes you want to wait for.

`waitForAll` - `true` if you want to wait for every mutex in the list, `false` if you only want to wait for one.

`time` - Just like `wait`, how long to wait for the lock to be granted. Does not default to `INFINITE`, however.

Refer to [MSDN](https://msdn.microsoft.com/en-us/library/windows/desktop/ms687025(v=vs.85).aspx) for details on the return value.

# [License](LICENSE)
