{
  "targets": [
    {
      "cflags!": [ "-fno-exceptions" ],
      "cflags_cc!": [ "-fno-exceptions" ],
      "include_dirs": ["<!(node -p \"require('node-addon-api').include_dir\")"],
      "target_name": "nodeeasyipc",
      "sources": ["addon.cc","filemap.cc","mutex.cc","ipc.cc"],
      'defines': ['NAPI_DISABLE_CPP_EXCEPTIONS']
    }
  ]
}