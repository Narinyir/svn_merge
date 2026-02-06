import subprocess


class SVNAdapter:

    @staticmethod
    def run_command(args, cwd=None):
        result = subprocess.run(
            args,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            raise Exception(result.stderr.strip())

        return result.stdout.strip()

    @staticmethod
    def get_head_revision(path):
        output = SVNAdapter.run_command(["svn", "info"], cwd=path)
        for line in output.splitlines():
            if line.startswith("Revision:"):
                return line.split(":")[1].strip()
        return None

    @staticmethod
    def is_working_copy_clean(path):
        output = SVNAdapter.run_command(["svn", "status"], cwd=path)
        return output.strip() == ""
    
    @staticmethod
    def get_log_summary(path, from_rev, to_rev):
        output = SVNAdapter.run_command([
            "svn", "log",
            "--summarize",
            "--xml",
            "-r", f"{from_rev}:{to_rev}"
        ], cwd=path)

        changes = []

        root = ET.fromstring(output)

        for logentry in root.findall("logentry"):
            revision = logentry.attrib["revision"]

            paths = logentry.find("paths")
            if paths is None:
                continue

            for p in paths.findall("path"):
                action = p.attrib.get("action")
                file_path = p.text

                changes.append({
                    "revision": revision,
                    "action": action,
                    "path": file_path
                })

        return changes