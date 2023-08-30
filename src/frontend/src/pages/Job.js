import axios from "axios";
import {baseUrl} from "../utils/ApiUtils";
import {useState, useEffect} from "react";
import {useParams} from "react-router-dom";
import JobStatus from "../components/JobStatus";

function Job() {
  const [job, setJob] = useState({"logs": ""});

  let { id } = useParams();

  function getJob() {
    axios
      .get(`${baseUrl}/jobs/${id}`)
      .then(({ data: response }) => {
        setJob(response)
      })
      .catch(error => {
        console.log(error)
      });
  }
  useEffect(() => {
    getJob(id)
  }, [id]);

  useEffect(() => {
    if (job && ["RUNNING", "PENDING"].includes(job.status)) {
      const interval = setInterval(() => {
        getJob(id)
      }, 2000);

      return () => clearInterval(interval);
    }
  }, [id, job]);

  return (
    <div>
      <div className="flex max-w-full min-h-full flex-row justify-center px-6 py-12 lg:px-8">
        <div className="divide-y flex-1 max-w-4xl divide-gray-100">
          <div className="mt-6 px-6 border-t border-gray-100">
            <dl className="divide-y divide-gray-100">
              <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
                <dt className="text-sm font-medium leading-6 text-gray-900">Job name</dt>
                <dd className="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{job.name}</dd>
              </div>
              <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
                <dt className="text-sm font-medium leading-6 text-gray-900">Status</dt>
                <dd className="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                  <div className="mt-1 flex items-center gap-x-1.5">
                    <JobStatus jobStatus={job?.status} />
                  </div>
                </dd>
              </div>
              <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
                <dt className="text-sm font-medium leading-6 text-gray-900">Run type</dt>
                <dd className="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{job.run_type}</dd>
              </div>
              <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
                <dt className="text-sm font-medium leading-6 text-gray-900">Job ID</dt>
                <dd className="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{job.id}</dd>
              </div>
              {job.image &&
              <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
                <dt className="text-sm font-medium leading-6 text-gray-900">Docker Image</dt>
                <dd className="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{job.image}</dd>
              </div>
              }

              <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
                <dt className="text-sm font-medium leading-6 text-gray-900">Command</dt>
                <dd className="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                  {job?.command?.split("\n").map((line, index) => <div key={index}>{line}</div>)}
                </dd>
              </div>
            </dl>
          </div>
        </div>
        <div className="flex-1 max-w-4xl divide-gray-100 mt-6 px-6 border-t border-gray-100">
          <div className=" border-gray-300 border-2 mx-2 px-2">
            <div className="text-2xl my-2">Logs</div>
            <code className="whitespace-pre mx-2 my-2 px-2 py-2">
              {job.logs.split(/\r?\n/)
                .filter(line =>!!line)
                .map((line, index) => (
                <div
                  key={index}
                  className={
                    "flex " +
                    (index % 2 ? "bg-gray-100" : "bg-gray-200"
                    )}
                >
                  <span className="ml-2 max-w-10 w-8 text-right">{index + 1}</span>
                  <span className="ml-6 w-full">{line}</span>
                </div>
              ))}
            </code>
          </div>
        </div>
      </div>
    </div>
  );
}
export default Job
