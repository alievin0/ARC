# Webots Cloud build image.
#
# webots.cloud reads the version from the FROM line of this file to decide
# which Webots release to run the simulation with. R2023b matches the
# "#VRML_SIM R2023b utf8" header of worlds/mini_arc2.wbt.
#
# PROJECT_PATH is supplied by webots.cloud at build time; the whole repository
# is copied there so that worlds/ and controllers/ keep their relative layout,
# which is how Webots resolves controller "mini_arc2".

FROM cyberbotics/webots.cloud:R2023b-ubuntu22.04
ARG PROJECT_PATH
RUN mkdir -p $PROJECT_PATH
COPY . $PROJECT_PATH
