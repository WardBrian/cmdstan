include_directories(../../lib/CLI11-1.9.1) # TODO better CLI11
include_directories(.. ${rapidjson_INCLUDE_DIR} ${stan_INCLUDE_DIR})

add_executable(stansummary stansummary.cpp)
target_link_libraries(stansummary PRIVATE
  StanMath::stanmath)
  set_target_properties(stansummary PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/bin)

add_executable(diagnose diagnose.cpp)
target_link_libraries(diagnose PRIVATE
  StanMath::stanmath)
set_target_properties(diagnose PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/bin)

add_library(cmdstan_main OBJECT main.cpp)
target_link_libraries(cmdstan_main PUBLIC
  StanMath::stanmath)
target_precompile_headers(cmdstan_main PUBLIC
  ${stan_INCLUDE_DIR}/stan/model/model_header.hpp)
