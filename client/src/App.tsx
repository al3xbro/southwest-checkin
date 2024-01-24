import axios from 'axios'
import { FieldErrors, useForm } from 'react-hook-form'
import { useMutation } from '@tanstack/react-query'

type ReserveFormData = {
    firstName: string,
    lastName: string,
    confirmation: string,
    date: string,
    time: string,
    email: string,
    meridiem: 'pm' | 'am',
}

type ReserveRequestData = {
    firstName: string,
    lastName: string,
    confirmation: string,
    dateTimeString: string,
    email: string,
}

function transformData(data: ReserveFormData): ReserveRequestData {
    const [month, day, year] = data.date.split('/')
    let [hour, minute] = data.time.split(':')
    if (data.meridiem === 'pm') {
        hour = String(Number(hour) + 12)
    }
    const dateTime = new Date(Number(year), Number(month) - 1, Number(day), Number(hour), Number(minute))
    return {
        firstName: data.firstName,
        lastName: data.lastName,
        confirmation: data.confirmation,
        dateTimeString: dateTime.toUTCString(),
        // TODO: change after adding email
        email: data.email ?? '',
    }
}

function displayErrors(errors: FieldErrors<ReserveFormData>) {
    return errors.firstName?.message ?? errors.lastName?.message ?? errors.confirmation?.message ?? errors.email?.message ?? errors.date?.message ?? errors.time?.message ?? errors.meridiem?.message ?? ''
}

function normalizeDate(date: string) {
    date = date.replace(/\D/g, '').slice(0, 8);
    if (date.length >= 5) {
        return `${date.slice(0, 2)}/${date.slice(2, 4)}/${date.slice(4)}`;
    }
    else if (date.length >= 3) {
        return `${date.slice(0, 2)}/${date.slice(2)}`;
    }
    return date
}

function normalizeTime(time: string) {
    return time.replace(/\D/g, '').match(/\d{1,2}/g)?.join(":").slice(0, 5) ?? ""
}

export default function App() {

    const { register, handleSubmit, getValues, setValue, formState: { errors } } = useForm<ReserveFormData>()
    const reserve = useMutation({
        mutationFn: (data: ReserveRequestData) => {
            return axios.post('https://alexserver.sytes.net:8001/reserve/', data, {
                headers: {
                    "Content-Type": "application/json",
                }
            })
        }
    })

    return (
        <>
            <div className='w-full h-full flex items-center justify-center bg-black'>
                <form
                    className='text-white border-2 border-white rounded-xl flex flex-col gap-5
                    p-[25px] w-full m-[20px]
                    sm:p-[50px] sm:max-w-[700px]'
                    onSubmit={handleSubmit((data) => { reserve.mutate(transformData(data)) })}
                >
                    <div className='flex gap-5'>
                        <input className='p-3 bg-neutral-800 rounded-md w-full' type='text' placeholder='First Name' {...register('firstName', { required: { value: true, message: 'First name required.' } })} />
                        <input className='p-3 bg-neutral-800 rounded-md w-full' type='text' placeholder='Last Name' {...register('lastName', { required: { value: true, message: 'Last name required.' } })} />
                    </div>
                    <input className='p-3 bg-neutral-800 rounded-md w-full' type='text' placeholder='Confirmation Number' {...register('confirmation', { required: { value: true, message: 'Confirmation number required.' } })} />
                    {/* TODO: change after adding email */}
                    {/* <input className='p-3 bg-neutral-800 rounded-md w-full' type='text' placeholder='Email' inputMode='email' {...register('email', { required: { value: true, message: 'Email required.' } })} /> */}

                    {/* date */}
                    <div className='flex flex-col sm:flex-row gap-5'>
                        {/* input here */}
                        <input className='p-3 bg-neutral-800 rounded-md w-full' type='tel' inputMode='numeric' placeholder='mm/dd/yyyy' onChange={(e) => { setValue('date', normalizeDate(e.target.value)) }}
                            ref={register('date', {
                                required: {
                                    value: true,
                                    message: 'Valid date required.'
                                },
                                pattern: {
                                    value: /(0[1-9]|1[012])\/(0[1-9]|[12][0-9]|3[01])\/(19|20)\d{2}/,
                                    message: 'Valid date required.'
                                }
                            }).ref}
                        />
                        <div className='flex gap-5 w-full'>
                            <input className='p-3 bg-neutral-800 rounded-md w-full' type='tel' inputMode='numeric' placeholder='hh:mm' onChange={(e) => { setValue('time', normalizeTime(e.target.value)) }}
                                ref={register('time', {
                                    required: {
                                        value: true,
                                        message: 'Valid time required.'
                                    },
                                    pattern: {
                                        value: /^(0[0-9]|1[0-2]):[0-5][0-9]$/,
                                        message: 'Valid time required.'
                                    }
                                }).ref}
                            />
                            <select className='bg-neutral-800 rounded-md p-3' {...register('meridiem', { required: { value: true, message: 'Valid time required.' } })}>
                                <option value='am'>AM</option>
                                <option value='pm'>PM</option>
                            </select>
                        </div>
                    </div >

                    {/* submit and status */}
                    < div className='flex justify-between gap-5' >
                        {reserve.isSuccess ? <div className='text-green-500 my-auto'>{`You will automatically be checked in on ${getValues('date')} at ${getValues('time')} ${getValues('meridiem')}.`}</div> : null}
                        {reserve.isError ? <div className='text-red-500 my-auto'>An error occured contacting the server.</div> : null}
                        {reserve.isPending ? <div className='text-yellow-500 my-auto'>Loading...</div> : null}
                        {reserve.isIdle ? <div className='text-red-500 my-auto'>{displayErrors(errors)}</div> : null}
                        <button className='p-3 bg-neutral-800 rounded-md active:bg-neutral-700 sm:hover:bg-neutral-700 transition' type='submit'>Auto Reserve</button>
                    </div >
                </form >
            </div >
        </>
    )
}

