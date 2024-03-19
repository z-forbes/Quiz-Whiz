[← ← ←](../../../#full-usage)

After [installing the program](installation.md), follow these steps to see how the program functions.

## 1. Look at the example file
In your file explorer, open the file [`example_input.md`](example_input.md) within the `docs` directory. It should look like this:

<img src='example_input.png' width='50%'>

## 2. Decide on parameters
For this example, we'll pretend we're creating a file to be imported into Learn. As explained in the [complete usage instructions](complete_usage.md), this requires the `--learn` flag to be added. All other settings are uneccessary for this example.

## 3. Run the command 
After [opening the program in the terminal](https://www.wikihow.com/Open-a-Folder-in-Cmd), run `python3 main.py docs/example_input.md --learn`.

This should yield the following output:

<img src='images/example_program_output1.png' width='60%'>

## 4. Examine output & fix mistakes
Despite running with no errors, the program gave a warning because it detected a potential mistake. This mistake occured becasuse there is no newline between the question and answers in the first question of the example. To fix this and remove the warning, open the example input file and change the first question to:

```
# Which ocean is the warmest?

- ^Atlantic
- Pacific
- Arctic
```
Make sure to save the file after adding the newline.

## 5. Rerun the program
After fixing the mistake, run `python3 main.py docs/example_input.md --learn` again. There should now be no warnings, and the parse table shows one less essay question and one more multiple choice question, as a result of the first question now being parsed correctly.

<img src='images/example_program_output2.png' width='60%'>

## 6. Access the output
The file created by the program can be found in the `output` folder, and it's called `LEARN_example_input.txt`. It can be imported into Learn using these [upload isntructions](https://help.blackboard.com/Learn/Instructor/Ultra/Tests_Pools_Surveys/Reuse_Questions/Upload_Questions). The output should look like [this file](LEARN_example_input.txt).

To change where the output is saved, use the `--output` flag. For example, including `--output to_upload` will save the output to the `to_upload` directory.
