import React, { useState } from 'react';
import { makeReservation } from '../services/api';

interface ReservationFormProps {
    onSuccess: (id: number) => void;
    onCancel: () => void;
}

export const ReservationForm: React.FC<ReservationFormProps> = ({ onSuccess, onCancel }) => {
    const [formData, setFormData] = useState({
        name: '',
        phone: '',
        guests: 2,
        date: '',
        time: ''
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const response = await makeReservation(formData);
            if (response.status === 'confirmed') {
                onSuccess(response.reservation_id);
            }
        } catch (err: any) {
            if (err.response && err.response.data && err.response.data.detail) {
                setError(err.response.data.detail);
            } else {
                setError('Failed to make reservation. Please try a different time.');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="bg-white p-4 rounded shadow-md border border-gray-200">
            <h3 className="font-bold text-lg mb-2">Book a Table</h3>
            {error && <p className="text-red-500 text-sm mb-2">{error}</p>}
            <form onSubmit={handleSubmit} className="space-y-3">
                <input
                    type="text"
                    placeholder="Name"
                    required
                    className="w-full border p-2 rounded"
                    value={formData.name}
                    onChange={e => setFormData({ ...formData, name: e.target.value })}
                />
                <input
                    type="tel"
                    placeholder="Phone"
                    required
                    className="w-full border p-2 rounded"
                    value={formData.phone}
                    onChange={e => setFormData({ ...formData, phone: e.target.value })}
                />
                <div className="flex space-x-2">
                    <input
                        type="number"
                        min="1"
                        max="10"
                        required
                        className="w-1/3 border p-2 rounded"
                        value={formData.guests}
                        onChange={e => setFormData({ ...formData, guests: parseInt(e.target.value) })}
                    />
                    <input
                        type="date"
                        required
                        className="w-2/3 border p-2 rounded"
                        value={formData.date}
                        onChange={e => setFormData({ ...formData, date: e.target.value })}
                    />
                </div>
                <input
                    type="time"
                    required
                    className="w-full border p-2 rounded"
                    value={formData.time}
                    onChange={e => setFormData({ ...formData, time: e.target.value + (e.target.value.length === 5 ? ':00' : '') })}
                // Note: time input gives HH:MM, backend expects HH:MM:SS sometimes or HH:MM is fine depending on pydantic.
                // Pydantic Time type usually accepts HH:MM.
                />

                <div className="flex justify-end space-x-2">
                    <button type="button" onClick={onCancel} className="bg-gray-200 px-3 py-1 rounded">Cancel</button>
                    <button type="submit" disabled={loading} className="bg-primary text-white px-3 py-1 rounded hover:bg-secondary">
                        {loading ? 'Booking...' : 'Confirm'}
                    </button>
                </div>
            </form>
        </div>
    );
};
