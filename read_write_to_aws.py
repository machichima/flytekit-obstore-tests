import os

from flytekit import task, workflow, current_context, ImageSpec
from flytekit.types.file import FlyteFile


flytekit_hash = "7de4b411360bbb8371bca50f11e408f38a6db67d"
flytekit = f"git+https://github.com/machichima/flytekit.git@{flytekit_hash}"

image_spec = ImageSpec(
    packages=[flytekit, "obstore==0.3.0b9"],
    apt_packages=["git"],
    registry="localhost:30000",
    env={
        # ...put env variables here to set credentials
    },
)

# Remote path
remote_path_from = "s3://flyte-aws-s3-bucket/test.json"
# remote_path_from = "s3://my-s3-bucket/test.json"
remote_path_to = "s3://flyte-aws-s3-bucket/test_new.json"


@task(container_image=image_spec)
def create_ff(input_file: FlyteFile) -> FlyteFile:
    with open(input_file, "r") as f:
        content = f.read()
        print(content)

    return input_file


@task(container_image=image_spec)
def write_ff(input_file: FlyteFile, output_location: str = "") -> FlyteFile:
    out_path = os.path.join(
        current_context().working_directory,
        f"test_new.json",
    )
    with open(input_file, "r") as f:
        content = f.read()
        print(content)
    with open(out_path, mode="w") as output_file:
        output_file.write(content)

    if output_location:
        return FlyteFile(path=out_path, remote_path=output_location)
    else:
        return FlyteFile(path=out_path)


@workflow
def wf() -> FlyteFile:
    existed_file = FlyteFile(path=remote_path_from)
    result_file = create_ff(input_file=existed_file)
    out_file = write_ff(result_file, remote_path_to)
    # result_file = task_remove_column(input_file=shuffled_file, column_name="County")
    return out_file


if __name__ == "__main__":
    from flytekit.clis.sdk_in_container import pyflyte
    from click.testing import CliRunner

    runner = CliRunner()
    path = os.path.realpath(__file__)
    result = runner.invoke(
        pyflyte.main,
        [
            "run",
            path,
            "wf",
        ],
    )
    print("Local Execution: ", result.output)
    result = runner.invoke(
        pyflyte.main,
        [
            "run",
            "--remote",
            path,
            "wf",
        ],
    )
    print("Remote Execution: ", result.output)
