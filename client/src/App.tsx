import axios from 'axios'
import { useForm } from 'react-hook-form'
import { useMutation } from '@tanstack/react-query'

type ReserveFormData = {
    firstName: string,
    lastName: string,
    confirmation: string,
    month: number,
    day: number,
    year: number,
    hour: number,
    minute: number,
    email: string,
}

type ReserveRequestData = {
    firstName: string,
    lastName: string,
    confirmation: string,
    dateTimeString: string,
    email: string,
}

function transformData(data: ReserveFormData): ReserveRequestData {
    const dateTimeString = new Date(data.year, data.month, data.day, data.hour, data.minute).toISOString()
    return {
        firstName: data.firstName,
        lastName: data.lastName,
        confirmation: data.confirmation,
        dateTimeString,
        email: data.email,
    }
}

export default function App() {

    const { register, handleSubmit, getValues } = useForm<ReserveFormData>()
    const reserve = useMutation({
        mutationFn: (data: ReserveRequestData) => {
            return axios.post('http://localhost:8000/reserve', data)
        }
    })

    return (
        <>
            <div className='w-full h-full flex items-center justify-center bg-black'>
                <form className='text-white border-2 border-white rounded-xl flex flex-col gap-5
                p-[25px] w-full m-[20px]
                sm:p-[50px] sm:max-w-[700px]'
                    onSubmit={handleSubmit((data) => { reserve.mutate(transformData(data)) })}>
                    <div className='flex gap-5'>
                        <input className='p-3 bg-neutral-800 rounded-md w-full' type="text" placeholder='First Name' {...register("firstName")} />
                        <input className='p-3 bg-neutral-800 rounded-md w-full' type="text" placeholder='Last Name' {...register("lastName")} />
                    </div>
                    <input className='p-3 bg-neutral-800 rounded-md w-full' type="text" placeholder='Confirmation Number' {...register("confirmation")} />
                    <div className='flex gap-5 flex-col sm:flex-row'>
                        <div className='flex gap-5'>
                            <input className='p-3 bg-neutral-800 rounded-md w-full' type="text" {...register("month")} />
                            <input className='p-3 bg-neutral-800 rounded-md w-full' type="text" {...register("day")} />
                            <input className='p-3 bg-neutral-800 rounded-md w-full' type="text" {...register("year")} />
                        </div>
                        <div className='flex gap-5'>
                            <input className='p-3 bg-neutral-800 rounded-md w-full' type="text" {...register("hour")} />
                            <input className='p-3 bg-neutral-800 rounded-md w-full' type="text" {...register("minute")} />
                        </div>
                    </div>
                    <input className='p-3 bg-neutral-800 rounded-md w-full' type="text" placeholder='Email' {...register("email")} />
                    <div className='flex justify-between'>
                        {reserve.isSuccess ? <div className='text-green-500 my-auto'>Success! You will automatically be checked in at time here </div> : null}
                        {reserve.isError ? <div className='text-red-500 my-auto'>An error occured contacting the server.</div> : null}
                        {reserve.isPending ? <div className='text-yellow-500 my-auto'>Loading...</div> : null}
                        {reserve.isIdle ? <div /> : null}
                        <button className='p-3 bg-neutral-800 rounded-md active:bg-neutral-700 sm:hover:bg-neutral-700 transition' type="submit">Auto Reserve</button>
                    </div>
                </form>
            </div>
        </>
    )
}

