from conan.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(visual_runtimes=["MD", "MDd"])
    builder.add_common_builds(shared_option_name=False, pure_c=False)
    builder.run()
