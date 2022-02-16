import logging
from plumbum import cli
from server.server import create_app
from server.calculation import Calculation
from server.calculation_machine import CalculationMachine

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s: %(message)s")

class ServerCli(cli.Application):

    other_user_freq = cli.SwitchAttr("--other-user-freq",
                                     argtype=int,
                                     default=5,
                                     help="How often simulated users should start calculations, -1 for never.")

    other_user_cancel_freq = cli.SwitchAttr("--other-user-cancel",
                                            argtype=int,
                                            default=10,
                                            help="How often simulated users should cancl their calculations. -1 for never.")

    error_freq = cli.SwitchAttr("--error-freq",
                                argtype=int,
                                default=30,
                                help="How often errors should occur. -1 for never")
    
    seed = cli.SwitchAttr("--seed",
                          argtype=int,
                          default=5,
                          help="Number of running calculations to seed the machine with.")

    auth = cli.Flag("--no-auth",
                    default=True,
                    help="Provide this to allow HTTP requests that do not include the"
                    " user token returned from the /login route")

    @cli.positional(int)
    def main(self, port: int):

        machine = CalculationMachine()
        
        if self.error_freq != -1:
            logging.info(f"Simulating errors roughly every {self.error_freq} seconds")
            machine.simulate_errors(frequency=self.error_freq)

        if self.other_user_cancel_freq != -1:
            logging.info(f"Simulating other users cancelling calculations roughly every {self.other_user_cancel_freq} seconds.")
            machine.simulate_cancellations(frequency=self.other_user_cancel_freq)

        if self.other_user_freq != -1:
            logging.info(f"Simulating other users starting calculations roughly every {self.other_user_freq} seconds.")
            machine.simulate_other_users(frequency=self.other_user_freq)

        logging.info(f"Seeding machine with {self.seed} running calculations.")
        for _ in range(self.seed):
            machine.add(Calculation.random())

        app = create_app(machine=machine, auth=self.auth)
        app.run(port=port)
        logging.info(f"Server listening on port {port}")
            
if __name__ == '__main__':
    ServerCli.run()
