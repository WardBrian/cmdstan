#ifndef CMDSTAN_ARGUMENTS_ARG_MODEL_HPP
#define CMDSTAN_ARGUMENTS_ARG_MODEL_HPP

#include <cmdstan/arguments/singleton_argument.hpp>

namespace cmdstan {

class arg_model : public string_argument {
 public:
  arg_model() : string_argument() {
    _name = "model";
    _description = "Model file";
    _validity = "Path to existing file";
    _default = "\"\"";
    _default_value = "";
    _constrained = false;
    _good_value = "good";
    _value = _default_value;
  }
};

}  // namespace cmdstan
#endif
