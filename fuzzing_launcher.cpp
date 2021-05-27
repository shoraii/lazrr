#include <fstream>
#include <string>
#include <iostream>
#include <stdlib.h>

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  std::string input = std::string(reinterpret_cast<const char*>(data), size);

  std::ifstream gform;
  gform.open("gform.txt");
  std::string form;
  
  if (getline(gform, form)) {
    std::cout << "Found gform " << form << "\n";
    form = "python3 lazrr.py " + form + " --fuzzed=True";

    std::ofstream temp_file("responses.txt");
    temp_file << input;
    temp_file.close();

    system(form.c_str());
  }

  gform.close();
  return 0;
}
