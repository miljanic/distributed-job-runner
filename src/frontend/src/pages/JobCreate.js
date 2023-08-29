import axios from "axios";
import {baseUrl} from "../utils/ApiUtils";
import {useNavigate} from "react-router-dom";
import {useForm} from "react-hook-form";

function Jobs() {
  const navigate = useNavigate();
  const {
    register,
    handleSubmit,
    watch,
  } = useForm({
    name: "",
    command: "",
    run_type: "",
    image: "",
  });
  const watchRunType = watch("run_type")


  function createJob(data) {
    console.log(data)
    axios
      .post(`${baseUrl}/jobs/`, data)
      .then(({ data: response }) => {
        navigate("/jobs")
      })
      .catch(error => {
        console.log(error)
      });
  }

  return (
    <div className="flex min-h-full flex-1 flex-col justify-center px-6 lg:py-12 lg:px-8">
      <div className="mt-2 sm:mx-auto max-w-16xl">
        <form className="space-y-6" onSubmit={handleSubmit(createJob)}>
          <div className="space-y-12">
            <div className="border-b border-gray-900/10 pb-12">
              <h2 className="text-base font-semibold leading-7 text-gray-900">Create Job</h2>

              <div className="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
                <div className="sm:col-span-4">
                  <label htmlFor="name"
                         className="block text-sm font-medium leading-6 text-gray-900">Name</label>
                  <div className="mt-2">
                    <div
                      className="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600 sm:max-w-md">
                      <span
                        className="flex select-none items-center pl-3 text-gray-500 sm:text-sm"></span>
                      <input
                        type="text"
                        name="name"
                        id="name"
                        {...register("name")}
                        autoComplete="name"
                        className="block flex-1 border-0 bg-transparent py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6"
                        placeholder="Build and push image" />
                    </div>
                  </div>
                </div>
              </div>
            </div>


            <div className="border-b border-gray-900/10 pb-12">
              <h2 className="text-base font-semibold leading-7 text-gray-900">Run configuration</h2>
              <p className="mt-1 text-sm leading-6 text-gray-600">Configure Job running options.</p>

              <div className="mt-10 space-y-10">
                <fieldset>
                  <legend className="text-sm font-semibold leading-6 text-gray-900">Run type</legend>
                  <p className="mt-1 text-sm leading-6 text-gray-600">Configure if Job should be running on the Host machine or in the Docker container.</p>
                  <div className="mt-6 space-y-6">
                    <div className="flex items-center gap-x-3">
                      <input
                        id="docker"
                        type="radio"
                        value="docker"
                        {...register("run_type")}
                        className="h-4 w-4 border-gray-300 text-indigo-600 focus:ring-indigo-600"
                      />
                        <label htmlFor="docker"
                               className="block text-sm font-medium leading-6 text-gray-900">Docker</label>
                    </div>
                    <div className="flex items-center gap-x-3">
                      <input
                        id="host"
                        type="radio"
                        value="host"
                        {...register("run_type")}
                        className="h-4 w-4 border-gray-300 text-indigo-600 focus:ring-indigo-600"
                      />
                        <label htmlFor="host" className="block text-sm font-medium leading-6 text-gray-900">Host</label>
                    </div>
                  </div>
                </fieldset>
                {watchRunType === "docker" ? (
                  <fieldset>
                    <div className="mt-6 space-y-6">
                      <div className="col-span-full">
                        <label htmlFor="image" className="block text-sm font-medium leading-6 text-gray-900">Docker Image</label>
                        <div className="mt-2">
                          <input
                            type="text"
                            name="image"
                            id="image"
                            {...register("image")}
                            autoComplete="image"
                            className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                          />
                        </div>
                      </div>
                      <div className="mt-6 space-y-6">
                        <div className="col-span-full">
                          <label htmlFor="image" className="block text-sm font-medium leading-6 text-gray-900">Command</label>
                          <div className="mt-2">
                            <input
                              type="text"
                              name="command"
                              {...register("command")}
                              id="command"
                              autoComplete="command"
                              className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                  </fieldset>
                ) : (
                  <div className="col-span-full">
                    <label htmlFor="command" className="block text-sm font-medium leading-6 text-gray-900">Script</label>
                    <div className="mt-2">
                      <textarea
                        id="command"
                        name="command"
                        {...register("command")}
                        rows="3"
                        className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" />
                    </div>
                    <p className="mt-3 text-sm leading-6 text-gray-600">Script to run as a Job.</p>
                  </div>

                )}

              </div>
            </div>
          </div>

          <div className="mt-6 flex items-center justify-end gap-x-6">
            <button
              type="button"
              onClick={() => navigate(-1)}
              className="text-sm font-semibold leading-6 text-gray-900">
              Cancel
            </button>
            <button type="submit"
                    className="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Save
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
export default Jobs
