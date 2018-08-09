import os


def mount_disk(session):
    os.system('fusermount -u "{}"'.format(session.mount_dir))
    os.system(
        'google-drive-ocamlfuse -label "{}" -o uid=$(id -u),gid=$(id -g),allow_other "{}"'.format(
            session.user_name, session.mount_dir
        )
    )


def get_mount_directory():
    return os.system('mount -l -t fuse.google-drive-ocamlfuse')
