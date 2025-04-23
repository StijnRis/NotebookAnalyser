from processor.processor import Processor
import cProfile
import pstats

def main():
    processor = Processor()
    processor.run()

if __name__ == "__main__":
    cProfile.run("main()", sort="time", filename="output/profile.prof")

    stats = pstats.Stats("output/profile.prof")
    stats.strip_dirs()
    stats.sort_stats("cumtime")
    stats.print_stats(100)
