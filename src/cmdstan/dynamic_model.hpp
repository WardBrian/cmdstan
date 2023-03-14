#ifndef CMDSTAN_DYNAMIC_MODEL_HPP
#define CMDSTAN_DYNAMIC_MODEL_HPP

#include <stan/model/model_base.hpp>

#include <string>
#include <memory>
#include <dlfcn.h>
#include <iostream>

namespace cmdstan {

typedef stan::model::model_base &(*NEW_MODEL)(
    stan::io::var_context &data_context, unsigned int seed,
    std::ostream *msg_stream);

class DynamicModel {
 public:
  DynamicModel(std::string filename, int flags = RTLD_NOW)
      : filename(filename), flags(flags), handle(nullptr), new_model(nullptr) {}

  bool load_model() {
    if (!(handle = dlopen(filename.c_str(), flags))) {
      std::cerr << "Failed to load " << filename << ": " << dlerror()
                << std::endl;
      return false;
    }
    new_model = reinterpret_cast<NEW_MODEL>(dlsym(handle, "new_model"));
    if (!new_model) {
      std::cerr << "Failed to find symbol 'new_model': " << dlerror()
                << std::endl;
      return false;
    }
    return true;
  }

  ~DynamicModel() {
    if (handle) {
      if (dlclose(handle) != 0) {
        std::cerr << dlerror() << std::endl;
      } else {
        handle = nullptr;
      }
    }
  }

  NEW_MODEL new_model;

 private:
  std::string filename;
  int flags;
  void *handle;
};

}  // namespace cmdstan

#endif
