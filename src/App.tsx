import { useMemo, useState } from 'react';
import {
    ArrowRight,
    Bell,
    ChevronDown,
    CircleUserRound,
    Clock3,
    CloudSun,
    CreditCard,
    IndianRupee,
    Landmark,
    Leaf,
    MapPinned,
    Menu,
    Minus,
    MoonStar,
    Phone,
    Plus,
    Search,
    ShieldCheck,
    Sparkles,
    Star,
    TrainFront,
    TrainTrack,
    UserRound,
    Wallet,
    X,
} from 'lucide-react';

type Train = {
    number: string;
    name: string;
    departure: string;
    arrival: string;
    duration: string;
    seats: number;
    className: string;
    fare: number;
    from: string;
    to: string;
};

const sampleTrains: Train[] = [
    { number: '12447', name: 'Vande Bharat Express', from: 'New Delhi', to: 'Agra Cantt', departure: '06:10', arrival: '07:55', duration: '1h 45m', seats: 26, className: 'AC Chair Car', fare: 880 },
    { number: '12859', name: 'Rajdhani Express', from: 'New Delhi', to: 'Mumbai Central', departure: '16:20', arrival: '08:35', duration: '16h 15m', seats: 14, className: 'AC 3 Tier', fare: 1625 },
    { number: '12627', name: 'Kashi Vishwanath Express', from: 'Varanasi', to: 'New Delhi', departure: '22:15', arrival: '06:20', duration: '8h 05m', seats: 31, className: 'Sleeper', fare: 510 },
    { number: '12951', name: 'Maharaja Express', from: 'Delhi', to: 'Jaipur', departure: '08:00', arrival: '11:35', duration: '3h 35m', seats: 22, className: 'AC 2 Tier', fare: 1150 },
];

const quickActions = [
    { label: 'PNR Status', icon: Search },
    { label: 'Charts / Vacancy', icon: TrainTrack },
    { label: 'Train Schedule', icon: Clock3 },
    { label: 'Cancel Ticket', icon: X },
    { label: 'Refund Status', icon: Wallet },
];

const featureCards = [
    { label: 'Safety First', icon: ShieldCheck },
    { label: 'Secure Journey', icon: CreditCard },
    { label: 'On Time Always', icon: Sparkles },
];

const stats = [
    { value: '7,000+', label: 'Stations' },
    { value: '68,000+', label: 'Route Kilometres' },
    { value: '13,000+', label: 'Trains' },
    { value: 'Millions', label: 'Happy Passengers Everyday' },
];

function App() {
    const [isMobileNavOpen, setIsMobileNavOpen] = useState(false);
    const [isLoginOpen, setIsLoginOpen] = useState(false);
    const [from, setFrom] = useState('');
    const [to, setTo] = useState('');
    const [date, setDate] = useState('');
    const [travelClass, setTravelClass] = useState('All Classes');
    const [quota, setQuota] = useState('GENERAL');
    const [results, setResults] = useState<Train[]>([]);
    const [error, setError] = useState('');

    const currentDate = useMemo(() => new Date().toLocaleDateString('en-IN', {
        day: '2-digit',
        month: 'short',
        year: 'numeric'
    }), []);

    const handleSwap = () => {
        setFrom(to);
        setTo(from);
    };

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        if (!from.trim() || !to.trim()) {
            setError('Please enter source and destination stations.');
            return;
        }
        if (!date) {
            setError('Please select a journey date.');
            return;
        }

        const filtered = sampleTrains.filter((train) => {
            const matchFrom = train.from.toLowerCase().includes(from.trim().toLowerCase()) || train.from.toLowerCase().includes(from.trim().toLowerCase());
            const matchTo = train.to.toLowerCase().includes(to.trim().toLowerCase()) || train.to.toLowerCase().includes(to.trim().toLowerCase());
            return matchFrom && matchTo;
        });

        const finalResults = filtered.length > 0 ? filtered : sampleTrains.slice(0, 3);
        setResults(finalResults);
        setError('');
    };

    return (
        <div className="min-h-screen bg-slate-100 text-slate-900">
            <header className="sticky top-0 z-40 border-b border-sky-100 bg-white/85 backdrop-blur-xl">
                <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-between py-4">
                        <div className="flex items-center gap-4">
                            <div className="flex h-12 w-12 items-center justify-center rounded-full bg-rail-blue text-lg font-extrabold text-white shadow-md">
                                <TrainFront size={26} />
                            </div>
                            <div>
                                <p className="text-[11px] font-semibold uppercase tracking-[0.25em] text-rail-blue/70">Indian Railways</p>
                                <h1 className="text-xl font-black tracking-tight text-rail-blue">Lifeline of the Nation</h1>
                            </div>
                        </div>

                        <nav className="hidden items-center gap-6 text-sm font-medium text-slate-700 lg:flex">
                            {['Home', 'Trains', 'Meals', 'IRCTC E-Wallet', 'Charts / Vacancy', 'Alerts', 'Contact Us'].map((item) => (
                                <a key={item} href="#" className="transition hover:text-rail-orange">{item}</a>
                            ))}
                        </nav>

                        <div className="hidden items-center gap-4 lg:flex">
                            <div className="flex items-center gap-2 rounded-full border border-slate-200 bg-slate-50 px-3 py-2 text-xs text-slate-600">
                                <Clock3 size={14} /> {currentDate}
                            </div>
                            <button
                                onClick={() => setIsLoginOpen(true)}
                                className="rounded-full bg-rail-orange px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-orange-200 transition hover:-translate-y-0.5 hover:bg-orange-500"
                            >
                                Login / Register
                            </button>
                        </div>

                        <button
                            className="rounded-full border border-slate-200 p-2 lg:hidden"
                            onClick={() => setIsMobileNavOpen(!isMobileNavOpen)}
                            aria-label="Open mobile menu"
                        >
                            {isMobileNavOpen ? <X size={18} /> : <Menu size={18} />}
                        </button>
                    </div>

                    {isMobileNavOpen && (
                        <div className="space-y-3 border-t border-slate-200 py-4 lg:hidden">
                            {['Home', 'Trains', 'Meals', 'IRCTC E-Wallet', 'Charts / Vacancy', 'Alerts', 'Contact Us'].map((item) => (
                                <a key={item} href="#" className="block text-sm font-medium text-slate-700">{item}</a>
                            ))}
                        </div>
                    )}
                </div>
            </header>

            <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
                <section className="relative overflow-hidden rounded-[42px] bg-rail-gradient p-4 sm:p-6 lg:p-8">
                    <div className="absolute left-[-90px] top-10 h-52 w-52 rounded-full bg-sky-200/60 blur-3xl" />
                    <div className="absolute right-[-30px] bottom-[-20px] h-60 w-60 rounded-full bg-blue-200/60 blur-3xl" />

                    <div className="relative flex flex-col gap-8 lg:flex-row lg:items-center lg:justify-between">
                        <aside className="hidden lg:flex lg:w-24 lg:flex-col lg:items-center lg:gap-5">
                            {quickActions.map(({ label, icon: Icon }) => (
                                <button
                                    key={label}
                                    className="group flex w-20 flex-col items-center gap-2 rounded-full bg-white/80 p-3 text-center text-[10px] font-semibold uppercase tracking-wide text-slate-700 shadow-lg transition hover:-translate-y-1 hover:shadow-xl"
                                >
                                    <span className="flex h-11 w-11 items-center justify-center rounded-full bg-rail-blue text-white shadow-md transition group-hover:scale-105">
                                        <Icon size={18} />
                                    </span>
                                    <span>{label}</span>
                                </button>
                            ))}
                        </aside>

                        <div className="flex-1">
                            <div className="hero-oval rail-card soft-shadow relative mx-auto max-w-[760px] overflow-hidden border border-sky-100 bg-white/80 p-4 sm:p-6 lg:p-8">
                                <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,_rgba(14,116,144,0.12),transparent_35%)]" />
                                <div className="relative z-10">
                                    <div className="mb-6 flex flex-col gap-2 text-center">
                                        <p className="text-xs font-bold uppercase tracking-[0.28em] text-rail-blue/70">Book Train Ticket</p>
                                        <h2 className="text-3xl font-black tracking-tight text-rail-blue sm:text-4xl">Travel Safe | Travel Smart | Travel India</h2>
                                    </div>

                                    <form onSubmit={handleSearch} className="space-y-4">
                                        <div className="grid gap-3 md:grid-cols-2">
                                            <div className="relative">
                                                <label className="mb-2 block text-[11px] font-bold uppercase tracking-[0.2em] text-slate-600">From</label>
                                                <div className="flex items-center rounded-full border border-sky-200 bg-sky-50 px-4 py-3 shadow-inner shadow-sky-100">
                                                    <MapPinned className="mr-3 text-rail-blue" size={18} />
                                                    <input
                                                        value={from}
                                                        onChange={(e) => setFrom(e.target.value)}
                                                        className="w-full bg-transparent text-sm text-slate-700 outline-none placeholder:text-slate-400"
                                                        placeholder="Enter source station"
                                                    />
                                                </div>
                                            </div>

                                            <div className="relative">
                                                <label className="mb-2 block text-[11px] font-bold uppercase tracking-[0.2em] text-slate-600">To</label>
                                                <div className="flex items-center rounded-full border border-sky-200 bg-sky-50 px-4 py-3 shadow-inner shadow-sky-100">
                                                    <MapPinned className="mr-3 text-rail-blue" size={18} />
                                                    <input
                                                        value={to}
                                                        onChange={(e) => setTo(e.target.value)}
                                                        className="w-full bg-transparent text-sm text-slate-700 outline-none placeholder:text-slate-400"
                                                        placeholder="Enter destination station"
                                                    />
                                                </div>
                                            </div>
                                        </div>

                                        <div className="flex justify-center">
                                            <button
                                                type="button"
                                                onClick={handleSwap}
                                                className="flex h-12 w-12 items-center justify-center rounded-full border-4 border-white bg-rail-blue text-white shadow-lg shadow-blue-200 transition hover:scale-105"
                                                aria-label="Swap from and to"
                                            >
                                                <ArrowRight className="rotate-90" size={18} />
                                            </button>
                                        </div>

                                        <div className="grid gap-3 md:grid-cols-3">
                                            <div>
                                                <label className="mb-2 block text-[11px] font-bold uppercase tracking-[0.2em] text-slate-600">Journey Date</label>
                                                <input
                                                    type="date"
                                                    value={date}
                                                    onChange={(e) => setDate(e.target.value)}
                                                    className="w-full rounded-full border border-sky-200 bg-sky-50 px-4 py-3 text-sm text-slate-700 outline-none"
                                                />
                                            </div>

                                            <div>
                                                <label className="mb-2 block text-[11px] font-bold uppercase tracking-[0.2em] text-slate-600">Class</label>
                                                <div className="relative">
                                                    <select
                                                        value={travelClass}
                                                        onChange={(e) => setTravelClass(e.target.value)}
                                                        className="w-full appearance-none rounded-full border border-sky-200 bg-sky-50 px-4 py-3 text-sm text-slate-700 outline-none"
                                                    >
                                                        <option>All Classes</option>
                                                        <option>AC 2 Tier</option>
                                                        <option>AC 3 Tier</option>
                                                        <option>AC Chair Car</option>
                                                        <option>Sleeper</option>
                                                    </select>
                                                    <ChevronDown className="pointer-events-none absolute right-4 top-3.5 text-slate-500" size={16} />
                                                </div>
                                            </div>

                                            <div>
                                                <label className="mb-2 block text-[11px] font-bold uppercase tracking-[0.2em] text-slate-600">Quota</label>
                                                <div className="relative">
                                                    <select
                                                        value={quota}
                                                        onChange={(e) => setQuota(e.target.value)}
                                                        className="w-full appearance-none rounded-full border border-sky-200 bg-sky-50 px-4 py-3 text-sm text-slate-700 outline-none"
                                                    >
                                                        <option>GENERAL</option>
                                                        <option>TATKAL</option>
                                                        <option>PREMIUM TATKAL</option>
                                                        <option>WOMEN</option>
                                                    </select>
                                                    <ChevronDown className="pointer-events-none absolute right-4 top-3.5 text-slate-500" size={16} />
                                                </div>
                                            </div>
                                        </div>

                                        <div className="grid gap-3 pt-2 text-sm text-slate-700 md:grid-cols-3">
                                            {[
                                                'Person With Disability Concession',
                                                'Flexible With Date',
                                                'Railway Pass Concession',
                                            ].map((item) => (
                                                <label key={item} className="flex items-center gap-2 rounded-full bg-slate-50 px-3 py-2">
                                                    <input type="checkbox" className="h-4 w-4 accent-rail-orange" />
                                                    <span>{item}</span>
                                                </label>
                                            ))}
                                        </div>

                                        {error && <div className="rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-600">{error}</div>}

                                        <div className="pt-2 text-center">
                                            <button
                                                type="submit"
                                                className="rounded-full bg-rail-orange px-8 py-4 text-base font-bold text-white shadow-xl shadow-orange-200 transition hover:-translate-y-0.5 hover:bg-orange-500"
                                            >
                                                Search Trains →
                                            </button>
                                        </div>
                                    </form>
                                </div>
                            </div>
                        </div>

                        <aside className="flex flex-col items-center justify-center gap-6 lg:w-[250px]">
                            <div className="relative flex h-[320px] w-[320px] items-center justify-center rounded-[42%] border-[10px] border-[#d9eaff] bg-sky-50 p-3 shadow-soft">
                                <div className="absolute inset-6 rounded-[40%] border border-sky-200" />
                                <div className="train-visual relative h-full w-full overflow-hidden rounded-[42%] border-4 border-white shadow-xl">
                                    <div className="absolute left-5 top-5 z-10 flex items-center gap-2 rounded-full bg-white/80 px-3 py-2 text-[10px] font-bold uppercase tracking-[0.18em] text-rail-blue shadow-md">
                                        <Leaf size={12} className="text-green-600" />
                                        Indian Railways
                                    </div>
                                    <div className="absolute inset-0 bg-[linear-gradient(180deg,rgba(17,24,39,0.08),rgba(17,24,39,0.2)),url('https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=900&q=80')] bg-cover bg-center" />
                                    <div className="absolute inset-x-0 bottom-0 h-28 bg-gradient-to-t from-slate-900/55 to-transparent" />
                                    <div className="absolute bottom-6 left-6 right-6 z-10">
                                        <div className="flex items-center justify-between text-sm font-semibold text-white">
                                            <span>INDIAN RAILWAYS</span>
                                            <span className="inline-flex h-2 w-2 rounded-full bg-green-400" />
                                        </div>
                                        <p className="mt-2 text-xl font-black text-white">Connecting Every Corner of India</p>
                                    </div>
                                </div>
                            </div>

                            <div className="flex flex-wrap justify-center gap-4">
                                {featureCards.map(({ label, icon: Icon }) => (
                                    <div key={label} className="flex w-28 flex-col items-center gap-2 rounded-[28px] bg-white/80 px-3 py-4 text-center shadow-lg backdrop-blur-sm">
                                        <span className="flex h-11 w-11 items-center justify-center rounded-full bg-rail-blue text-white shadow-md">
                                            <Icon size={18} />
                                        </span>
                                        <span className="text-xs font-bold text-slate-700">{label}</span>
                                    </div>
                                ))}
                            </div>
                        </aside>
                    </div>

                    <div className="relative mt-10 grid gap-3 rounded-[32px] border border-sky-100 bg-white/75 p-3 backdrop-blur-md md:grid-cols-4">
                        {stats.map((item, index) => (
                            <div key={item.label} className="flex items-center justify-center gap-3 rounded-[24px] bg-white/80 px-4 py-5 text-center shadow-sm">
                                <span className="flex h-10 w-10 items-center justify-center rounded-full bg-sky-100 text-rail-blue">
                                    {index === 0 && <TrainFront size={18} />}
                                    {index === 1 && <Landmark size={18} />}
                                    {index === 2 && <TrainTrack size={18} />}
                                    {index === 3 && <Star size={18} />}
                                </span>
                                <div>
                                    <p className="text-xl font-black text-rail-blue">{item.value}</p>
                                    <p className="text-xs font-medium text-slate-600">{item.label}</p>
                                </div>
                            </div>
                        ))}
                    </div>

                    <div className="relative mt-6 flex items-center justify-center">
                        <div className="flex w-full max-w-5xl items-center justify-between gap-3 rounded-full bg-rail-blue px-6 py-4 text-white shadow-lg shadow-blue-200/50">
                            <div className="flex items-center gap-3">
                                <span className="flex h-10 w-10 items-center justify-center rounded-full bg-white/15"><Leaf size={18} /></span>
                                <p className="text-lg font-semibold">A Cleaner | Greener | Smarter India</p>
                            </div>
                            <span className="hidden sm:block text-sm text-sky-100">Sustainable mobility</span>
                        </div>
                    </div>
                </section>

                <section className="mt-12">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-xs font-bold uppercase tracking-[0.3em] text-rail-blue/70">Search Results</p>
                            <h3 className="mt-2 text-3xl font-black text-rail-blue">Available Trains</h3>
                        </div>
                        <div className="rounded-full bg-white px-4 py-2 text-sm font-medium text-slate-600 shadow-sm">{from || 'Delhi'} → {to || 'Agra'}</div>
                    </div>

                    <div className="mt-6 space-y-4">
                        {results.length === 0 ? (
                            <div className="rounded-[28px] border border-dashed border-sky-200 bg-white/60 p-10 text-center text-slate-500 shadow-sm">
                                Search for a route to view available trains.
                            </div>
                        ) : (
                            results.map((train) => (
                                <div key={train.number} className="rounded-[28px] border border-sky-100 bg-white p-5 shadow-soft transition hover:-translate-y-1 hover:shadow-2xl">
                                    <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
                                        <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
                                            <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-rail-blue text-xl font-black text-white shadow-md">
                                                {train.number.slice(0, 2)}
                                            </div>
                                            <div>
                                                <p className="text-xs font-bold uppercase tracking-[0.2em] text-slate-500">{train.number}</p>
                                                <h4 className="text-2xl font-black text-slate-900">{train.name}</h4>
                                            </div>
                                        </div>

                                        <div className="grid flex-1 gap-3 text-sm text-slate-600 sm:grid-cols-3 lg:grid-cols-5">
                                            <div>
                                                <p className="text-[11px] font-bold uppercase tracking-[0.18em] text-slate-500">Departure</p>
                                                <p className="mt-1 text-xl font-black text-rail-blue">{train.departure}</p>
                                            </div>
                                            <div>
                                                <p className="text-[11px] font-bold uppercase tracking-[0.18em] text-slate-500">Arrival</p>
                                                <p className="mt-1 text-xl font-black text-rail-blue">{train.arrival}</p>
                                            </div>
                                            <div>
                                                <p className="text-[11px] font-bold uppercase tracking-[0.18em] text-slate-500">Duration</p>
                                                <p className="mt-1 text-base font-bold">{train.duration}</p>
                                            </div>
                                            <div>
                                                <p className="text-[11px] font-bold uppercase tracking-[0.18em] text-slate-500">Seats</p>
                                                <p className="mt-1 text-base font-bold text-emerald-600">{train.seats} left</p>
                                            </div>
                                            <div>
                                                <p className="text-[11px] font-bold uppercase tracking-[0.18em] text-slate-500">Fare</p>
                                                <p className="mt-1 text-lg font-black text-rail-blue">₹{train.fare}</p>
                                            </div>
                                        </div>

                                        <div className="flex items-center gap-3">
                                            <div className="rounded-full bg-sky-50 px-3 py-2 text-xs font-bold uppercase tracking-[0.2em] text-slate-600">{train.className}</div>
                                            <button className="rounded-full bg-rail-orange px-5 py-3 text-sm font-bold text-white shadow-lg shadow-orange-200 transition hover:bg-orange-500">
                                                Book Now
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            ))
                        )}
                    </div>
                </section>
            </main>

            {isLoginOpen && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 p-4 backdrop-blur-sm">
                    <div className="w-full max-w-md rounded-[28px] bg-white p-6 shadow-2xl">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-xs font-bold uppercase tracking-[0.25em] text-rail-blue/70">Welcome</p>
                                <h3 className="mt-1 text-2xl font-black text-rail-blue">Login / Register</h3>
                            </div>
                            <button onClick={() => setIsLoginOpen(false)} className="rounded-full bg-slate-100 p-2 text-slate-600">
                                <X size={18} />
                            </button>
                        </div>

                        <div className="mt-6 space-y-4">
                            <label className="block">
                                <span className="mb-2 block text-sm font-medium text-slate-600">Mobile Number or Email</span>
                                <input className="w-full rounded-full border border-sky-200 bg-sky-50 px-4 py-3 outline-none" placeholder="Enter your email" />
                            </label>
                            <label className="block">
                                <span className="mb-2 block text-sm font-medium text-slate-600">Password</span>
                                <input type="password" className="w-full rounded-full border border-sky-200 bg-sky-50 px-4 py-3 outline-none" placeholder="Password" />
                            </label>
                            <button className="w-full rounded-full bg-rail-orange px-5 py-3 text-base font-bold text-white shadow-lg shadow-orange-200">Login</button>
                            <button className="w-full rounded-full border border-sky-200 bg-sky-50 px-5 py-3 text-base font-semibold text-rail-blue">Create New Account</button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default App;
