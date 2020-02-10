from commands import *

working_path = Path.combine(Path.working(), "load")

for root, dirs, files in OS.walk(working_path):
    for file in files:
        if File.get_extension(file) == ".log":
            filepath = Path.combine(root, file)
            lines = Str.nl(File.read(filepath))

            # clean
            while "Average:" in lines[-1]:
                lines.remove(lines[-1])
            File.write(filepath, newline.join(lines)+newline, mode="w")
            # end clean

            avg = {"thr": [], "mem": [], "cpu": []}
            for line in lines:
                ints = Str.get_integers(line)
                print(line)
                if ints:
                    avg["thr"].append(ints[-1])
                    avg["mem"].append(ints[-2])
                    avg["cpu"].append(ints[-3])
            Print.prettify(avg)
            string = f"Average:\t\t\t\t\t\tcpu:{sum(avg['cpu'])/len(avg['cpu']):.2f}%\t" \
                     f"mem:{sum(avg['mem'])/len(avg['mem']):.2f}Mb\t" \
                     f"thr:{sum(avg['thr'])/len(avg['thr']):.2f}"
            print(string)
            File.write(filepath, string, mode="a")
