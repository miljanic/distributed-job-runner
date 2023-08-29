import axios from "axios";
import {baseUrl} from "../utils/ApiUtils";
import {useState, useEffect} from "react";
import {useNavigate} from "react-router-dom";
import JobStatus from "../components/JobStatus";
import Dropdown from "../components/Dropdown";

const runTypeImages = {
  docker: "/docker.svg",
  host: "/host.svg"
}
function Jobs() {
  const navigate = useNavigate();

  const [filters, setFilters] = useState({
    run_type: "",
    status: ""
  })
  function setFilter(field, value) {
    setFilters({
      ...filters,
      [field]: filters[field] === value ? "" : value
    })
  }
  function getJobs() {
    axios
      .get(`${baseUrl}/jobs/`)
      .then(({ data: response }) => {
        setJobs(response)
      })
      .catch(error => {
        console.log(error)
      });
  }

  const [jobs, setJobs] = useState([]);
  useEffect(() => {
    getJobs()
  }, [])

  function matchesFilter(field, job) {
    return filters[field] === "" || job[field] === filters[field]
  }

  let filteredJobs = jobs.filter(job => {
    return Object.keys(filters).every(field => matchesFilter(field, job))
  }).sort((a,b) => a.created_at < b.created_at ? 1 : -1)

  return (
    <div className="flex justify-center">
      <div className="flex max-w-4xl min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
        <div className="flex justify-end">
          <Dropdown
            title="Status"
            setFilter={(value) => setFilter("status", value)}
            values={["running", "fail", "pending", "success"]}
          />
          <Dropdown
            title="Run type"
            setFilter={(value) => setFilter("run_type", value)}
            values={["docker", "host"]}
          />
        </div>
        <ul className="divide-y divide-gray-100 mt-4">
          {filteredJobs.map((job) => (
            <li key={job.id} className="flex justify-between gap-x-6 py-5 hover:bg-gray-200" onClick={() => navigate(`/jobs/${job.id}`)}>
              <div className="flex min-w-0 gap-x-4 ml-2">
                <img className="h-12 w-12 flex-none bg-transparent" src={runTypeImages[job.run_type]} alt="" />
                <div className="min-w-0 flex-auto">
                  <p className="text-sm font-semibold leading-6 text-gray-900">{job.name}</p>
                  <p className="mt-1 truncate text-xs leading-5 text-gray-500">Run type: {job.run_type}</p>
                </div>
              </div>
              <div className="hidden shrink-0 sm:flex justify-center sm:flex-col sm:items-end mr-2">
                <JobStatus jobStatus={job.status} />
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
export default Jobs
