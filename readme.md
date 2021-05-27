# lazrr
> 'Destroy Them With Lazers' - Knife Party, 2011

Google Forms autofill script

Installation:

`
    pip3 install -r requirements.txt
`

Usage:

`
    python3 lazrr.py https://docs.google.com/forms/d/e/.../viewform
`

Random strings will be placed in elements that require text responses. If you want to customize text responses, please specify them in `responses.txt`

Powered by [vvd170501/python-gforms](https://github.com/vvd170501/python-gforms)

# libfuzzer extra kek
> 'See a gform, day ruined' - BoloniniD right now

So, we use libfuzzer to generate random inputs.

Installation:
`
    sudo apt-get install clang
`

or any other way to install clang to your system.

Compilation:

`
    clang fuzzing_launcher.cpp -o lazrr -fsanitize=fuzzer,address
`

Usage:

Set the google form address in gform.txt. Set the initial corpus for libfuzzer in corpus directory. libfuzzer will generate random responses based on files in corpus. By default the corpus consists of `responses[sample].txt`.s

Launch lazrr with:

`
   ./lazrr --jobs=1 --workers=1 corpus --only_ascii=1 -reduce_inputs=0 --len_control=0
` 
