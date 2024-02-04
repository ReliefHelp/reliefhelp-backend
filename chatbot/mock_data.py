js = '''
{
    "Console.Writeline('Hello world');": "The code snippet you provided is written in C#. C# is a programming language developed by Microsoft and is commonly used for developing a wide range of applications, including desktop, web, and mobile applications. In this code, the Console.WriteLine statement is used to output the text 'Hello world' to the console.",
    "System.out.println('Hello world');": "The code snippet you provided is written in Java. Java is a popular programming language developed by Sun Microsystems (now owned by Oracle) and is widely used for developing various types of applications, including desktop, web, and mobile applications. In this code, the System.out.println statement is used to print the text 'Hello world!' to the standard output (console).",
    "fmt.Print('Hello world')": "The code snippet you provided is written in Go. Go (also known as Golang) is a statically typed, compiled programming language developed by Google. In this code, the fmt.Print function is used to print the text 'Hello world' to the standard output.",
    "print('Hello world')": "The code snippet you provided is written in Python. Python is a high-level, interpreted programming language known for its simplicity and readability. In this code, the print function is used to display the text 'Hello world' on the standard output.",
    "println!('Hello world')": "The code snippet you provided is written in Rust. Rust is a systems programming language known for its focus on safety, performance, and concurrency. In this code, the println! macro is used to print the text 'Hello world' to the standard output with a newline character."
}
'''
import json

json_data = json.loads(js)