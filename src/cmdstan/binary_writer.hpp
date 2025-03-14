#ifndef CMDSTAN_BINARY_WRITER_HPP
#define CMDSTAN_BINARY_WRITER_HPP

#include <stan/math/prim/fun/Eigen.hpp>
#include <stan/callbacks/writer.hpp>

#include <stdexcept>
#include <string>
#include <cstdint>

namespace cmdstan {
namespace io {

static const uint32_t MAGIC_NUMBER = 0x4E415453;  // "STAN"

template <typename Stream, typename Deleter = std::default_delete<Stream>>
class binary_writer final : public stan::callbacks::writer {
 public:
  explicit binary_writer(std::unique_ptr<Stream, Deleter> &&output)
      : output_(std::move(output)) {
    if (output_) {
      output_->write(reinterpret_cast<const char *>(&MAGIC_NUMBER),
                     sizeof(uint32_t));
    }
  };

  binary_writer() = default;
  binary_writer(binary_writer &other) = delete;
  binary_writer(binary_writer &&other) : output_(std::move(other.output_)) {}

  virtual ~binary_writer() {};

  /**
   * Primary method used by the Stan algorithms
   */
  void operator()(const std::vector<double> &v) override {
    if (output_) {
      const auto v_size = v.size();
      if (v_size != columns) {
        throw std::runtime_error(
            "Vector size does not match number of columns. Please report a "
            "bug!");
      }

      output_->write(reinterpret_cast<const char *>(v.data()),
                     sizeof(double) * v_size);
    }
  }

  /**
   * Used by Pathfinder which writes draws all at once
   */
  void operator()(const Eigen::MatrixXd &m) override {
    if (output_) {
      Eigen::MatrixXd d = m.transpose();
      if (d.cols() != columns) {
        throw std::runtime_error(
            "Matrix columns do not match output number of columns. Please "
            "report a "
            "bug!");
      }

      output_->write(reinterpret_cast<const char *>(d.data()),
                     sizeof(double) * d.size());
    }
  }

  void operator()(const Eigen::VectorXd &v) override {
    if (output_) {
      Eigen::RowVectorXd rv = v.transpose();

      if (rv.cols() != columns) {
        throw std::runtime_error(
            "Matrix columns do not match output number of columns. Please "
            "report a "
            "bug!");
      }

      output_->write(reinterpret_cast<const char *>(rv.data()),
                     sizeof(double) * rv.size());
    }
  }

  void operator()(const Eigen::RowVectorXd &rv) override {
    if (output_) {
      throw std::runtime_error(
          "Matrix columns do not match output number of columns. Please "
          "report a "
          "bug!");

      output_->write(reinterpret_cast<const char *>(rv.data()),
                     sizeof(double) * rv.size());
    }
  }

  void operator()(const std::vector<std::string> &names) {
    if (output_) {
      if (written_header) {
        throw std::runtime_error(
            "Header already written. Please report a bug!");
      }
      written_header = true;
      columns = names.size();
      std::string header = boost::algorithm::join(names, ",");
      uint64_t header_size = header.size() + 1;
      output_->write(reinterpret_cast<const char *>(&header_size),
                     sizeof(uint64_t));
      output_->write(header.c_str(), header_size);
      // pad to next multiple of 8
      uint64_t padding = 8 - ((12 + header_size) % 8);
      static const char zero = '\0';
      for (uint64_t i = 0; i < padding; ++i) {
        output_->write(&zero, 1);
      }
    }
  }

  bool is_valid() const noexcept { return output_ != nullptr; }

  void operator()() {}

  void operator()(const std::string &message) {}

 private:
  std::unique_ptr<Stream, Deleter> output_;
  uint64_t columns;
  bool written_header = false;
};

}  // namespace io
}  // namespace cmdstan

#endif
