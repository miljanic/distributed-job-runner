function JobStatus({ jobStatus }) {
  let status = jobStatus ? jobStatus.toUpperCase() : ""

  return <>
    {status === "RUNNING" && (
      <div className="mt-1 flex items-center gap-x-1.5">
        <div className="flex-none rounded-full bg-sky-500/20 p-1">
          <div className="h-1.5 w-1.5 rounded-full bg-sky-500" />
        </div>
        <p className="text-xs leading-5 text-gray-500">Running</p>
      </div>
    )}
    {status === "PENDING" && (
      <div className="mt-1 flex items-center gap-x-1.5">
        <div className="flex-none rounded-full bg-gray-500/20 p-1">
          <div className="h-1.5 w-1.5 rounded-full bg-gray-500" />
        </div>
        <p className="text-xs leading-5 text-gray-500">Pending</p>
      </div>
    )}
    {status === "SUCCESS" && (
      <div className="mt-1 flex items-center gap-x-1.5">
        <div className="flex-none rounded-full bg-emerald-500/20 p-1">
          <div className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
        </div>
        <p className="text-xs leading-5 text-gray-500">Succeeded</p>
      </div>
    )}
    {status === "FAIL" && (
      <div className="mt-1 flex items-center gap-x-1.5">
        <div className="flex-none rounded-full bg-red-500/20 p-1">
          <div className="h-1.5 w-1.5 rounded-full bg-red-500" />
        </div>
        <p className="text-xs leading-5 text-gray-500">Failed</p>
      </div>
    )}
  </>
}

export default JobStatus
