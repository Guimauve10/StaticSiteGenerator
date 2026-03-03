from textnode import TextNode

def main():
    dummy = TextNode("Dummy", "Plain", "Test.html")
    boot_test = TextNode("This is some anchor text", "link", "https://www.boot.dev")
    print(boot_test)

main()