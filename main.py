from processor.processor import Processor
import cProfile
import pstats

def main():
    processor = Processor()
    processor.run()

def profile():
    cProfile.run("main()", sort="time", filename="output/profile.prof")

    stats = pstats.Stats("output/profile.prof")
    stats.strip_dirs()
    stats.sort_stats("cumtime")
    stats.print_stats(20)

if __name__ == "__main__":
    profile()
