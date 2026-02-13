import React, { useState, useEffect } from 'react';
import { getMenu } from '../services/api';
import axios from 'axios';

interface MenuItem {
    id: number;
    name: string;
    category: string;
    price: number;
    is_veg: boolean;
    description: string;
    available: boolean;
}

export const MenuComponent: React.FC = () => {
    const [menuItems, setMenuItems] = useState<MenuItem[]>([]);
    const [loading, setLoading] = useState(false);
    const [stats, setStats] = useState<any>(null);

    const fetchMenu = async (compressed: boolean) => {
        setLoading(true);
        const startTime = performance.now();
        try {
            if (compressed) {
                // Fetch compressed stats to show savings
                const response = await axios.get('http://localhost:8000/menu/compressed');
                setStats(response.data);
            }

            // Always fetch standard menu for display
            const data = await getMenu();
            setMenuItems(data);

        } catch (error) {
            console.error("Error fetching menu:", error);
        } finally {
            const endTime = performance.now();
            if (!stats) {
                // If not compressed stats, just show time
                console.log(`Fetch time: ${endTime - startTime}ms`);
            }
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchMenu(true);
    }, []);

    return (
        <div className="bg-white p-6 rounded-lg shadow-md max-w-2xl mx-auto mt-4">
            <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold text-gray-800">Our Menu</h2>
                <button
                    onClick={() => fetchMenu(true)}
                    className="text-sm bg-primary text-white px-3 py-1 rounded hover:opacity-90 transition"
                >
                    Refresh & Compare
                </button>
            </div>

            {stats && (
                <div className="mb-4 bg-orange-100 p-3 rounded text-sm text-amber-900 border border-amber-200">
                    <p className="font-semibold">Compression Optimization:</p>
                    <p>Original Size: {stats.original_size_bytes} bytes</p>
                    <p>Compressed Size: {stats.compressed_size_bytes} bytes</p>
                    <p>Ratio: {stats.compression_ratio}</p>
                    <p>Time Taken: {stats.time_taken_ms} ms</p>
                </div>
            )}

            {loading ? (
                <div className="text-center py-4">Loading menu...</div>
            ) : (
                <div className="space-y-4">
                    {menuItems.map((item) => (
                        <div key={item.id} className="border-b border-gray-100 pb-2 last:border-0 flex justify-between">
                            <div>
                                <h3 className="font-semibold text-lg">{item.name} {item.is_veg && <span className="text-green-600 text-xs bg-green-100 px-1 rounded ml-2">VEG</span>}</h3>
                                <p className="text-gray-500 text-sm">{item.description}</p>
                            </div>
                            <div className="text-primary font-bold">
                                ${item.price}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};
